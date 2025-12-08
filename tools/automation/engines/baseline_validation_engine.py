#!/usr/bin/env python3
"""
SynergyMesh Baseline Validation Engine
======================================
Purpose: Validate baseline configurations and system health
Extracted from legacy validate-all-baselines.v1.0.sh and adapted for SynergyMesh
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Data class for validation results"""
    check_name: str
    status: str  # PASS, FAIL, WARN
    message: str
    details: Dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class BaselineValidationEngine:
    """Engine for validating SynergyMesh baseline configurations"""
    
    def __init__(self, namespace: str = "synergymesh-system"):
        self.namespace = namespace
        self.validation_results: List[ValidationResult] = []
        self.log_file = f"/tmp/baseline-validation-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
        
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        with open(self.log_file, 'a') as f:
            f.write(log_entry + "\n")
    
    def add_result(self, check_name: str, status: str, message: str, details: Dict = None):
        """Add validation result"""
        result = ValidationResult(
            check_name=check_name,
            status=status,
            message=message,
            details=details or {}
        )
        self.validation_results.append(result)
        
        emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        self.log(f"{emoji} {check_name}: {message}", level=status)
    
    def run_kubectl(self, args: List[str]) -> Tuple[bool, str]:
        """Execute kubectl command"""
        try:
            result = subprocess.run(
                ["kubectl"] + args,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout
        except Exception as e:
            return False, str(e)
    
    def check_prerequisites(self) -> bool:
        """Check if required tools are available"""
        self.log("Checking prerequisites...")
        
        # Check kubectl
        success, _ = self.run_kubectl(["version", "--client"])
        if not success:
            self.add_result("prerequisites", "FAIL", "kubectl not found")
            return False
        
        # Check cluster connectivity
        success, _ = self.run_kubectl(["cluster-info"])
        if not success:
            self.add_result("prerequisites", "FAIL", "Cannot connect to Kubernetes cluster")
            return False
        
        self.add_result("prerequisites", "PASS", "All prerequisites met")
        return True
    
    def validate_namespace(self) -> bool:
        """Validate namespace configuration"""
        self.log(f"Validating namespace: {self.namespace}")
        
        # Check namespace exists
        success, output = self.run_kubectl(["get", "namespace", self.namespace])
        if not success:
            self.add_result("namespace_exists", "FAIL", f"Namespace not found: {self.namespace}")
            return False
        
        self.add_result("namespace_exists", "PASS", f"Namespace exists: {self.namespace}")
        
        # Check namespace labels
        success, output = self.run_kubectl([
            "get", "namespace", self.namespace,
            "-o", "jsonpath={.metadata.labels}"
        ])
        
        if success:
            try:
                labels = json.loads(output) if output else {}
                required_labels = ["app.kubernetes.io/name"]
                missing_labels = [label for label in required_labels if label not in labels]
                
                if missing_labels:
                    self.add_result(
                        "namespace_labels",
                        "WARN",
                        f"Missing recommended labels: {missing_labels}",
                        {"labels": labels}
                    )
                else:
                    self.add_result("namespace_labels", "PASS", "All required labels present")
            except json.JSONDecodeError:
                self.add_result("namespace_labels", "WARN", "Could not parse namespace labels")
        
        return True
    
    def validate_configmaps(self) -> bool:
        """Validate ConfigMaps in namespace"""
        self.log("Validating ConfigMaps...")
        
        success, output = self.run_kubectl([
            "get", "configmap",
            "-n", self.namespace,
            "-o", "json"
        ])
        
        if not success:
            self.add_result("configmaps", "FAIL", "Could not retrieve ConfigMaps")
            return False
        
        try:
            data = json.loads(output)
            configmaps = data.get("items", [])
            
            if len(configmaps) == 0:
                self.add_result("configmaps", "WARN", "No ConfigMaps found")
            else:
                self.add_result(
                    "configmaps",
                    "PASS",
                    f"Found {len(configmaps)} ConfigMaps",
                    {"count": len(configmaps)}
                )
            
            return True
        except json.JSONDecodeError:
            self.add_result("configmaps", "FAIL", "Could not parse ConfigMap data")
            return False
    
    def validate_deployments(self) -> bool:
        """Validate Deployments in namespace"""
        self.log("Validating Deployments...")
        
        success, output = self.run_kubectl([
            "get", "deployment",
            "-n", self.namespace,
            "-o", "json"
        ])
        
        if not success:
            self.add_result("deployments", "WARN", "Could not retrieve Deployments")
            return True
        
        try:
            data = json.loads(output)
            deployments = data.get("items", [])
            
            if len(deployments) == 0:
                self.add_result("deployments", "WARN", "No Deployments found")
                return True
            
            ready_deployments = 0
            for deployment in deployments:
                name = deployment.get("metadata", {}).get("name", "unknown")
                status = deployment.get("status", {})
                ready_replicas = status.get("readyReplicas", 0)
                replicas = status.get("replicas", 0)
                
                if ready_replicas == replicas and replicas > 0:
                    ready_deployments += 1
            
            if ready_deployments == len(deployments):
                self.add_result(
                    "deployments",
                    "PASS",
                    f"All {len(deployments)} Deployments are ready"
                )
            else:
                self.add_result(
                    "deployments",
                    "WARN",
                    f"Only {ready_deployments}/{len(deployments)} Deployments are ready"
                )
            
            return True
        except json.JSONDecodeError:
            self.add_result("deployments", "FAIL", "Could not parse Deployment data")
            return False
    
    def validate_services(self) -> bool:
        """Validate Services in namespace"""
        self.log("Validating Services...")
        
        success, output = self.run_kubectl([
            "get", "service",
            "-n", self.namespace,
            "-o", "json"
        ])
        
        if not success:
            self.add_result("services", "WARN", "Could not retrieve Services")
            return True
        
        try:
            data = json.loads(output)
            services = data.get("items", [])
            
            if len(services) == 0:
                self.add_result("services", "WARN", "No Services found")
            else:
                self.add_result(
                    "services",
                    "PASS",
                    f"Found {len(services)} Services",
                    {"count": len(services)}
                )
            
            return True
        except json.JSONDecodeError:
            self.add_result("services", "FAIL", "Could not parse Service data")
            return False
    
    def validate_network_policies(self) -> bool:
        """Validate NetworkPolicies in namespace"""
        self.log("Validating NetworkPolicies...")
        
        success, output = self.run_kubectl([
            "get", "networkpolicy",
            "-n", self.namespace,
            "-o", "json"
        ])
        
        if not success:
            self.add_result("network_policies", "WARN", "Could not retrieve NetworkPolicies")
            return True
        
        try:
            data = json.loads(output)
            policies = data.get("items", [])
            
            if len(policies) == 0:
                self.add_result("network_policies", "WARN", "No NetworkPolicies found")
            else:
                self.add_result(
                    "network_policies",
                    "PASS",
                    f"Found {len(policies)} NetworkPolicies"
                )
            
            return True
        except json.JSONDecodeError:
            self.add_result("network_policies", "FAIL", "Could not parse NetworkPolicy data")
            return False
    
    def generate_report(self) -> Dict:
        """Generate validation report"""
        total_checks = len(self.validation_results)
        passed_checks = sum(1 for r in self.validation_results if r.status == "PASS")
        failed_checks = sum(1 for r in self.validation_results if r.status == "FAIL")
        warned_checks = sum(1 for r in self.validation_results if r.status == "WARN")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "namespace": self.namespace,
            "total_checks": total_checks,
            "passed": passed_checks,
            "failed": failed_checks,
            "warnings": warned_checks,
            "results": [
                {
                    "check": r.check_name,
                    "status": r.status,
                    "message": r.message,
                    "details": r.details,
                    "timestamp": r.timestamp
                }
                for r in self.validation_results
            ]
        }
        
        return report
    
    def run_all_validations(self) -> bool:
        """Run all validation checks"""
        self.log("=" * 60)
        self.log("SynergyMesh Baseline Validation")
        self.log("=" * 60)
        self.log(f"Namespace: {self.namespace}")
        self.log(f"Log File: {self.log_file}")
        self.log("")
        
        if not self.check_prerequisites():
            return False
        
        # Run all validations
        self.validate_namespace()
        self.validate_configmaps()
        self.validate_deployments()
        self.validate_services()
        self.validate_network_policies()
        
        # Generate and display report
        report = self.generate_report()
        
        self.log("")
        self.log("=" * 60)
        self.log("VALIDATION SUMMARY")
        self.log("=" * 60)
        self.log(f"Total Checks: {report['total_checks']}")
        self.log(f"✅ Passed: {report['passed']}")
        self.log(f"❌ Failed: {report['failed']}")
        self.log(f"⚠️  Warnings: {report['warnings']}")
        self.log("")
        
        # Save JSON report
        json_file = f"/tmp/baseline-validation-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)
        self.log(f"JSON report saved to: {json_file}")
        
        if report['failed'] == 0:
            self.log("🎉 All validations passed!")
            return True
        else:
            self.log("⚠️  Some validations failed")
            return False


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="SynergyMesh Baseline Validation Engine")
    parser.add_argument(
        "--namespace",
        default="synergymesh-system",
        help="Kubernetes namespace to validate"
    )
    
    args = parser.parse_args()
    
    engine = BaselineValidationEngine(namespace=args.namespace)
    success = engine.run_all_validations()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
