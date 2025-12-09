#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Adaptive Governance System

Dynamically adjusts governance rules and processes based on:
- Market/environment changes
- Risk profile changes
- Performance metrics
- Business velocity

Adapts:
- Decision approval levels
- Process speed/rigor balance
- Resource allocation
- Compliance strictness
- Timeline expectations
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import math


class EnvironmentIndicator(Enum):
    """Environmental indicators triggering adaptation"""
    MARKET_VOLATILITY = "market_volatility"
    RISK_LEVEL = "risk_level"
    ERROR_RATE = "error_rate"
    DECISION_VELOCITY = "decision_velocity"
    RESOURCE_UTILIZATION = "resource_utilization"
    COMPLIANCE_VIOLATIONS = "compliance_violations"


@dataclass
class EnvironmentMetrics:
    """Current environment metrics"""
    market_volatility: float              # 0-1, 0=stable, 1=chaotic
    risk_level: float                    # 0-1
    error_rate: float                    # 0-1
    decision_velocity: float             # decisions/hour
    resource_utilization: float          # 0-1
    compliance_violations: float         # violations/day
    timestamp: datetime


@dataclass
class AdaptationRule:
    """Rule for adapting governance"""
    trigger_condition: Callable[[EnvironmentMetrics], bool]
    adaptations: Dict[str, Any]  # What to change
    priority: int                # Higher = applied first


class AdaptiveGovernor:
    """Manages adaptive governance"""

    def __init__(self):
        """Initialize adaptive governor"""
        self.current_metrics: Optional[EnvironmentMetrics] = None
        self.adaptation_rules: List[AdaptationRule] = []
        self.active_adaptations: Dict[str, Any] = self._default_configuration()
        self._build_adaptation_rules()

    def _default_configuration(self) -> Dict[str, Any]:
        """Default governance configuration"""
        return {
            "decision_approval_levels": 2,           # 1-4
            "approval_timeout_hours": 24,            # How long to wait
            "process_parallelism": "sequential",     # sequential, parallel, hybrid
            "test_coverage_requirement": 80,         # Percentage
            "deployment_frequency": "weekly",        # daily, weekly, monthly
            "rollback_enabled": True,
            "compliance_strictness": "standard",     # lenient, standard, strict
            "risk_tolerance": 0.5,                   # 0-1
            "change_batch_size": "standard",         # small, standard, large
            "monitoring_frequency": 300,             # seconds
        }

    def _build_adaptation_rules(self) -> None:
        """Build all adaptation rules"""

        # Rule 1: High market volatility → Accelerate decisions
        def high_volatility(metrics: EnvironmentMetrics) -> bool:
            return metrics.market_volatility > 0.7

        self.adaptation_rules.append(AdaptationRule(
            trigger_condition=high_volatility,
            adaptations={
                "decision_approval_levels": 1,
                "approval_timeout_hours": 4,
                "process_parallelism": "parallel",
                "change_batch_size": "large",
                "deployment_frequency": "daily"
            },
            priority=10
        ))

        # Rule 2: High error rate → Increase rigor
        def high_errors(metrics: EnvironmentMetrics) -> bool:
            return metrics.error_rate > 0.05

        self.adaptation_rules.append(AdaptationRule(
            trigger_condition=high_errors,
            adaptations={
                "decision_approval_levels": 4,
                "approval_timeout_hours": 48,
                "test_coverage_requirement": 95,
                "process_parallelism": "sequential",
                "compliance_strictness": "strict",
                "rollback_enabled": True
            },
            priority=9
        ))

        # Rule 3: High risk level → Increase monitoring
        def high_risk(metrics: EnvironmentMetrics) -> bool:
            return metrics.risk_level > 0.7

        self.adaptation_rules.append(AdaptationRule(
            trigger_condition=high_risk,
            adaptations={
                "monitoring_frequency": 60,  # More frequent
                "decision_approval_levels": 3,
                "compliance_strictness": "strict",
                "risk_tolerance": 0.2
            },
            priority=8
        ))

        # Rule 4: Low resource utilization → Optimize
        def low_utilization(metrics: EnvironmentMetrics) -> bool:
            return metrics.resource_utilization < 0.3

        self.adaptation_rules.append(AdaptationRule(
            trigger_condition=low_utilization,
            adaptations={
                "process_parallelism": "parallel",
                "deployment_frequency": "daily",
                "change_batch_size": "large"
            },
            priority=5
        ))

        # Rule 5: High compliance violations → Tighten
        def high_violations(metrics: EnvironmentMetrics) -> bool:
            return metrics.compliance_violations > 2.0

        self.adaptation_rules.append(AdaptationRule(
            trigger_condition=high_violations,
            adaptations={
                "compliance_strictness": "strict",
                "approval_timeout_hours": 72,
                "test_coverage_requirement": 100,
                "monitoring_frequency": 30
            },
            priority=7
        ))

        # Rule 6: High decision velocity → Optimize flow
        def high_velocity(metrics: EnvironmentMetrics) -> bool:
            return metrics.decision_velocity > 20  # decisions/hour

        self.adaptation_rules.append(AdaptationRule(
            trigger_condition=high_velocity,
            adaptations={
                "process_parallelism": "parallel",
                "decision_approval_levels": 1,
                "approval_timeout_hours": 1
            },
            priority=6
        ))

    def update_metrics(self, metrics: EnvironmentMetrics) -> None:
        """Update environment metrics and adapt if needed"""
        self.current_metrics = metrics
        self._apply_adaptations()

    def _apply_adaptations(self) -> None:
        """Apply adaptation rules based on current metrics"""
        if self.current_metrics is None:
            return

        # Start with defaults
        new_config = self._default_configuration()

        # Apply matching rules in priority order
        matching_rules = [
            rule for rule in self.adaptation_rules
            if rule.trigger_condition(self.current_metrics)
        ]

        # Sort by priority (descending)
        matching_rules.sort(key=lambda r: r.priority, reverse=True)

        # Apply adaptations
        for rule in matching_rules:
            new_config.update(rule.adaptations)

        self.active_adaptations = new_config

    def get_adapted_configuration(self) -> Dict[str, Any]:
        """Get current adapted configuration"""
        return self.active_adaptations.copy()

    def get_approval_level(self) -> int:
        """Get current approval level (1-4)"""
        return self.active_adaptations.get("decision_approval_levels", 2)

    def get_approval_timeout(self) -> int:
        """Get approval timeout in hours"""
        return self.active_adaptations.get("approval_timeout_hours", 24)

    def get_test_coverage_requirement(self) -> int:
        """Get test coverage requirement percentage"""
        return self.active_adaptations.get("test_coverage_requirement", 80)

    def get_compliance_strictness(self) -> str:
        """Get compliance strictness level"""
        return self.active_adaptations.get("compliance_strictness", "standard")

    def should_allow_parallel_execution(self) -> bool:
        """Can processes run in parallel?"""
        parallelism = self.active_adaptations.get("process_parallelism", "sequential")
        return parallelism in ["parallel", "hybrid"]

    def get_monitoring_frequency_seconds(self) -> int:
        """Get monitoring frequency in seconds"""
        return self.active_adaptations.get("monitoring_frequency", 300)

    def get_risk_tolerance(self) -> float:
        """Get risk tolerance (0-1)"""
        return self.active_adaptations.get("risk_tolerance", 0.5)

    def get_deployment_frequency(self) -> str:
        """Get deployment frequency"""
        return self.active_adaptations.get("deployment_frequency", "weekly")

    def explain_current_adaptation(self) -> str:
        """Explain why current adaptations are active"""
        if self.current_metrics is None:
            return "No metrics available"

        explanations = []

        for rule in self.adaptation_rules:
            if rule.trigger_condition(self.current_metrics):
                explanations.append(self._explain_rule(rule))

        if not explanations:
            return "Running with default configuration"

        return "Active adaptations:\n" + "\n".join(f"  • {exp}" for exp in explanations)

    def _explain_rule(self, rule: AdaptationRule) -> str:
        """Generate explanation for a rule"""
        # Find which condition triggered
        if rule.trigger_condition == self.adaptation_rules[0].trigger_condition:
            return "High market volatility: Accelerating decision process"
        elif rule.trigger_condition == self.adaptation_rules[1].trigger_condition:
            return "High error rate detected: Increasing process rigor"
        elif rule.trigger_condition == self.adaptation_rules[2].trigger_condition:
            return "High risk level: Increasing monitoring"
        else:
            return "Governance rules adapted"

    def report_metrics(self) -> str:
        """Report current metrics"""
        if self.current_metrics is None:
            return "No metrics available"

        metrics = self.current_metrics
        report = [
            "📊 Environment Metrics:",
            f"  Market Volatility: {metrics.market_volatility:.1%}",
            f"  Risk Level: {metrics.risk_level:.1%}",
            f"  Error Rate: {metrics.error_rate:.1%}",
            f"  Decision Velocity: {metrics.decision_velocity:.1f} decisions/hour",
            f"  Resource Utilization: {metrics.resource_utilization:.1%}",
            f"  Compliance Violations: {metrics.compliance_violations:.1f}/day"
        ]

        return "\n".join(report)

    def report_configuration(self) -> str:
        """Report current configuration"""
        config = self.get_adapted_configuration()
        report = [
            "⚙️  Current Governance Configuration:",
            f"  Approval Levels: {config.get('decision_approval_levels')}",
            f"  Approval Timeout: {config.get('approval_timeout_hours')}h",
            f"  Test Coverage: {config.get('test_coverage_requirement')}%",
            f"  Compliance Strictness: {config.get('compliance_strictness')}",
            f"  Parallelism: {config.get('process_parallelism')}",
            f"  Deployment Frequency: {config.get('deployment_frequency')}",
            f"  Risk Tolerance: {config.get('risk_tolerance'):.1%}"
        ]

        return "\n".join(report)
