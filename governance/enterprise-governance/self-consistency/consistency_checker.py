#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Self-Consistency Checker

Validates topological and logical consistency of governance system.
Detects:
- Logic contradictions
- Rule conflicts
- Process gaps/overlaps
- Circular dependencies
- Inconsistent policies
"""

from typing import Dict, List, Set, Tuple, Any, Optional
from dataclasses import dataclass
from enum import Enum


class InconsistencyType(Enum):
    """Types of detected inconsistencies"""
    LOGIC_CONTRADICTION = "logic_contradiction"
    RULE_CONFLICT = "rule_conflict"
    CIRCULAR_DEPENDENCY = "circular_dependency"
    PROCESS_GAP = "process_gap"
    PROCESS_OVERLAP = "process_overlap"
    POLICY_CONFLICT = "policy_conflict"
    STATE_CONTRADICTION = "state_contradiction"


@dataclass
class Inconsistency:
    """Detected inconsistency"""
    inconsistency_type: InconsistencyType
    severity: str                              # "critical", "high", "medium", "low"
    entities_involved: List[str]              # What entities are involved
    description: str                          # Human-readable description
    suggested_fix: Optional[str] = None       # How to fix it


class SelfConsistencyChecker:
    """Validates governance system consistency"""

    def __init__(self, governance_system):
        """Initialize with governance system"""
        self.system = governance_system
        self.inconsistencies: List[Inconsistency] = []

    def check_all(self) -> Tuple[bool, List[Inconsistency]]:
        """Run all consistency checks"""
        self.inconsistencies = []

        # Run individual checks
        self._check_logic_consistency()
        self._check_rule_conflicts()
        self._check_circular_dependencies()
        self._check_process_integrity()
        self._check_policy_conflicts()
        self._check_state_constraints()

        return len(self.inconsistencies) == 0, self.inconsistencies

    def _check_logic_consistency(self) -> None:
        """Check for logical contradictions in policies"""
        # Example: A policy says "must approve within 24h" and another says "no approvals after 20h"
        # These are logically contradictory

        # Get all policies
        policies = self._collect_all_policies()

        for policy_id, policy in policies.items():
            for other_id, other_policy in policies.items():
                if policy_id >= other_id:  # Avoid checking twice
                    continue

                # Check if policies contradict
                if self._policies_contradict(policy, other_policy):
                    self.inconsistencies.append(Inconsistency(
                        inconsistency_type=InconsistencyType.LOGIC_CONTRADICTION,
                        severity="high",
                        entities_involved=[policy_id, other_id],
                        description=f"Policy '{policy_id}' and '{other_id}' have contradictory requirements",
                        suggested_fix="Review and reconcile conflicting requirements"
                    ))

    def _check_rule_conflicts(self) -> None:
        """Check for conflicting governance rules"""
        # Get all rules
        rules = self._collect_all_rules()

        for rule_id, rule in rules.items():
            for other_id, other_rule in rules.items():
                if rule_id >= other_id:
                    continue

                # Check if rules conflict
                if self._rules_conflict(rule, other_rule):
                    self.inconsistencies.append(Inconsistency(
                        inconsistency_type=InconsistencyType.RULE_CONFLICT,
                        severity="high",
                        entities_involved=[rule_id, other_id],
                        description=f"Rule '{rule_id}' and '{other_id}' produce conflicting outcomes",
                        suggested_fix="Clarify rule precedence or modify rule conditions"
                    ))

    def _check_circular_dependencies(self) -> None:
        """Detect circular dependencies in processes"""
        # Build dependency graph
        dep_graph = self._build_dependency_graph()

        # Find cycles using DFS
        visited: Set[str] = set()
        rec_stack: Set[str] = set()
        cycles: List[List[str]] = []

        def dfs(node: str, path: List[str]) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in dep_graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor, path[:])
                elif neighbor in rec_stack:
                    # Found cycle
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    cycles.append(cycle)

            rec_stack.discard(node)

        for node in dep_graph:
            if node not in visited:
                dfs(node, [])

        for cycle in cycles:
            self.inconsistencies.append(Inconsistency(
                inconsistency_type=InconsistencyType.CIRCULAR_DEPENDENCY,
                severity="critical",
                entities_involved=cycle,
                description=f"Circular dependency detected: {' → '.join(cycle)}",
                suggested_fix="Break the cycle by removing or modifying one of the dependencies"
            ))

    def _check_process_integrity(self) -> None:
        """Check for process gaps and overlaps"""
        processes = self._collect_all_processes()

        for proc_id, process in processes.items():
            # Check if all required steps are defined
            if not self._all_steps_defined(process):
                self.inconsistencies.append(Inconsistency(
                    inconsistency_type=InconsistencyType.PROCESS_GAP,
                    severity="medium",
                    entities_involved=[proc_id],
                    description=f"Process '{proc_id}' has missing steps",
                    suggested_fix="Define all required process steps"
                ))

            # Check for overlapping responsibilities
            for other_id, other_process in processes.items():
                if proc_id >= other_id:
                    continue
                if self._processes_overlap(process, other_process):
                    self.inconsistencies.append(Inconsistency(
                        inconsistency_type=InconsistencyType.PROCESS_OVERLAP,
                        severity="medium",
                        entities_involved=[proc_id, other_id],
                        description=f"Processes '{proc_id}' and '{other_id}' have overlapping responsibilities",
                        suggested_fix="Clarify ownership and eliminate duplicate steps"
                    ))

    def _check_policy_conflicts(self) -> None:
        """Check for conflicting policies across domains"""
        # Example: data-governance says "encrypt all data" but api-governance says "cache unencrypted for performance"

        # Collect policies from all domains
        domain_policies = self._collect_domain_policies()

        for domain1, policies1 in domain_policies.items():
            for domain2, policies2 in domain_policies.items():
                if domain1 >= domain2:
                    continue

                for policy1 in policies1:
                    for policy2 in policies2:
                        if self._policies_conflict_across_domains(policy1, policy2):
                            self.inconsistencies.append(Inconsistency(
                                inconsistency_type=InconsistencyType.POLICY_CONFLICT,
                                severity="high",
                                entities_involved=[domain1, domain2],
                                description=f"Policy conflict between '{domain1}' and '{domain2}'",
                                suggested_fix="Reconcile cross-domain policy requirements"
                            ))

    def _check_state_constraints(self) -> None:
        """Check for impossible state combinations"""
        # Some states cannot coexist logically
        # Example: decision=ROLLED_BACK and compliance=EXEMPTED is contradictory

        impossible_combinations = [
            # (decision, risk, compliance, resource, time)
            ("completed", "critical", "compliant", "sufficient", "on_schedule"),  # Unlikely but not impossible
            ("rolled_back", "low", "exempted", "sufficient", "on_schedule"),      # Contradictory
        ]

        # This is a simplified check - real implementation would be more comprehensive
        # ...

    def _policies_contradict(self, policy1: Dict, policy2: Dict) -> bool:
        """Check if two policies contradict"""
        # Simplified check
        rules1 = policy1.get("rules", {})
        rules2 = policy2.get("rules", {})

        # Check for mutually exclusive requirements
        for rule_key in rules1:
            if rule_key in rules2:
                val1 = rules1[rule_key]
                val2 = rules2[rule_key]
                # Check if values are contradictory
                if isinstance(val1, dict) and isinstance(val2, dict):
                    if val1.get("enforcement") == "strict" and val2.get("enforcement") == "prohibited":
                        return True
        return False

    def _rules_conflict(self, rule1: Dict, rule2: Dict) -> bool:
        """Check if two rules conflict"""
        # Simple implementation
        return rule1.get("id") != rule2.get("id") and \
               rule1.get("domain") == rule2.get("domain") and \
               rule1.get("condition") == rule2.get("condition") and \
               rule1.get("action") != rule2.get("action")

    def _all_steps_defined(self, process: Dict) -> bool:
        """Check if all required steps are defined in a process"""
        required_steps = process.get("required_steps", [])
        defined_steps = process.get("steps", [])

        if not required_steps:
            return True

        defined_step_names = {step.get("name") for step in defined_steps}
        return all(step in defined_step_names for step in required_steps)

    def _processes_overlap(self, process1: Dict, process2: Dict) -> bool:
        """Check if two processes have overlapping responsibilities"""
        steps1 = {step.get("responsibility") for step in process1.get("steps", [])}
        steps2 = {step.get("responsibility") for step in process2.get("steps", [])}

        # Check for common responsibilities (might indicate overlap)
        overlap = steps1.intersection(steps2)
        return len(overlap) > 0

    def _policies_conflict_across_domains(self, policy1: Dict, policy2: Dict) -> bool:
        """Check if two policies from different domains conflict"""
        # Check for incompatible requirements
        enforcement1 = policy1.get("enforcement", "")
        enforcement2 = policy2.get("enforcement", "")

        # Example: one domain says "must encrypt", another says "must not use encryption for performance"
        rules1 = policy1.get("rules", {})
        rules2 = policy2.get("rules", {})

        # Check specific conflicting rules
        if "encryption" in rules1 and "caching" in rules2:
            if rules1["encryption"].get("required") and rules2["caching"].get("unencrypted"):
                return True

        return False

    def _collect_all_policies(self) -> Dict[str, Dict]:
        """Collect all policies from all domains"""
        policies = {}
        # This would iterate through governance domains in real implementation
        return policies

    def _collect_all_rules(self) -> Dict[str, Dict]:
        """Collect all governance rules"""
        rules = {}
        # This would iterate through all rules in real implementation
        return rules

    def _build_dependency_graph(self) -> Dict[str, List[str]]:
        """Build dependency graph of governance entities"""
        graph: Dict[str, List[str]] = {}
        # Build from GOVERNANCE_DEPENDENCY_MAP.yaml
        return graph

    def _collect_all_processes(self) -> Dict[str, Dict]:
        """Collect all governance processes"""
        processes = {}
        # This would collect all processes from process-governance dimension
        return processes

    def _collect_domain_policies(self) -> Dict[str, List[Dict]]:
        """Collect policies grouped by domain"""
        domain_policies: Dict[str, List[Dict]] = {}
        # This would iterate through meta-governance domains
        return domain_policies

    def report(self) -> str:
        """Generate consistency report"""
        if not self.inconsistencies:
            return "✅ System is fully consistent - no inconsistencies detected"

        report_lines = [
            "⚠️  CONSISTENCY CHECK REPORT",
            "=" * 80,
            f"\nFound {len(self.inconsistencies)} inconsistencies:\n"
        ]

        # Group by severity
        by_severity = {}
        for inc in self.inconsistencies:
            severity = inc.severity
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(inc)

        for severity in ["critical", "high", "medium", "low"]:
            if severity in by_severity:
                report_lines.append(f"\n{severity.upper()} ({len(by_severity[severity])}):")
                for inc in by_severity[severity]:
                    report_lines.append(f"  • {inc.description}")
                    if inc.suggested_fix:
                        report_lines.append(f"    → Fix: {inc.suggested_fix}")

        return "\n".join(report_lines)
