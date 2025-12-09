#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Multi-Dimensional State Space

Defines the 5-dimensional state space for governance decisions:
- Decision State (待审批, 已批准, 执行中, 已完成, 已回滚)
- Risk State (低, 中, 高, 临界, 未知)
- Compliance State (合规, 违规, 需要修改, 待验证, 豁免)
- Resource State (充足, 不足, 优化, 监控, 预警)
- Time State (按计划, 延迟, 加速, 阻滞, 取消)

Total: 5×5×5×5×5 = 3,125 possible states
"""

from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, Optional, Any
from enum import Enum
from datetime import datetime
import json


class DecisionState(Enum):
    """Decision execution states"""
    PENDING_APPROVAL = "pending_approval"      # 待审批
    APPROVED = "approved"                      # 已批准
    IN_EXECUTION = "in_execution"              # 执行中
    COMPLETED = "completed"                    # 已完成
    ROLLED_BACK = "rolled_back"               # 已回滚


class RiskState(Enum):
    """Risk assessment states"""
    LOW = "low"                                # 低
    MEDIUM = "medium"                         # 中
    HIGH = "high"                             # 高
    CRITICAL = "critical"                     # 临界
    UNKNOWN = "unknown"                       # 未知


class ComplianceState(Enum):
    """Compliance states"""
    COMPLIANT = "compliant"                   # 合规
    NON_COMPLIANT = "non_compliant"          # 违规
    NEEDS_MODIFICATION = "needs_modification" # 需要修改
    PENDING_VERIFICATION = "pending_verification" # 待验证
    EXEMPTED = "exempted"                     # 豁免


class ResourceState(Enum):
    """Resource availability states"""
    SUFFICIENT = "sufficient"                 # 充足
    INSUFFICIENT = "insufficient"            # 不足
    OPTIMIZING = "optimizing"                 # 优化中
    MONITORING = "monitoring"                 # 监控中
    ALERT = "alert"                           # 预警


class TimeState(Enum):
    """Timeline execution states"""
    ON_SCHEDULE = "on_schedule"               # 按计划
    DELAYED = "delayed"                       # 延迟
    ACCELERATED = "accelerated"               # 加速
    BLOCKED = "blocked"                       # 阻滞
    CANCELLED = "cancelled"                   # 取消


@dataclass
class StateCoordinate:
    """5D state coordinate"""
    decision: DecisionState
    risk: RiskState
    compliance: ComplianceState
    resource: ResourceState
    time: TimeState

    def __hash__(self) -> int:
        """Make hashable for set/dict operations"""
        return hash((self.decision, self.risk, self.compliance, self.resource, self.time))

    def __eq__(self, other) -> bool:
        """Equality check"""
        if not isinstance(other, StateCoordinate):
            return False
        return (
            self.decision == other.decision and
            self.risk == other.risk and
            self.compliance == other.compliance and
            self.resource == other.resource and
            self.time == other.time
        )

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary"""
        return {
            "decision": self.decision.value,
            "risk": self.risk.value,
            "compliance": self.compliance.value,
            "resource": self.resource.value,
            "time": self.time.value
        }

    def to_string(self) -> str:
        """Convert to readable string"""
        return f"[D:{self.decision.value} | R:{self.risk.value} | C:{self.compliance.value} | Rs:{self.resource.value} | T:{self.time.value}]"


@dataclass
class StateSnapshot:
    """Snapshot of entity state at a point in time"""
    entity_id: str
    entity_type: str                          # "decision", "governance_dimension", "process"
    coordinate: StateCoordinate
    timestamp: datetime
    metadata: Dict[str, Any]                  # Additional context
    triggered_by: Optional[str] = None        # What caused this state change
    triggering_event: Optional[str] = None


class StateSpace:
    """Manages the 5D state space"""

    # Valid state transitions
    VALID_TRANSITIONS = {
        DecisionState.PENDING_APPROVAL: [DecisionState.APPROVED, DecisionState.ROLLED_BACK],
        DecisionState.APPROVED: [DecisionState.IN_EXECUTION, DecisionState.ROLLED_BACK],
        DecisionState.IN_EXECUTION: [DecisionState.COMPLETED, DecisionState.ROLLED_BACK],
        DecisionState.COMPLETED: [DecisionState.ROLLED_BACK],  # Can be rolled back even after completion
        DecisionState.ROLLED_BACK: []  # Terminal state
    }

    # Risk transitions (allowed progressions)
    RISK_ESCALATION_PATH = [
        RiskState.UNKNOWN, RiskState.LOW, RiskState.MEDIUM, RiskState.HIGH, RiskState.CRITICAL
    ]

    def __init__(self):
        """Initialize state space"""
        self.snapshots: Dict[str, List[StateSnapshot]] = {}  # entity_id -> snapshots
        self.current_states: Dict[str, StateCoordinate] = {}  # entity_id -> current coordinate

    def initialize_entity(self, entity_id: str, entity_type: str) -> StateCoordinate:
        """Initialize an entity at default starting state"""
        initial_state = StateCoordinate(
            decision=DecisionState.PENDING_APPROVAL,
            risk=RiskState.UNKNOWN,
            compliance=ComplianceState.PENDING_VERIFICATION,
            resource=ResourceState.MONITORING,
            time=TimeState.ON_SCHEDULE
        )

        snapshot = StateSnapshot(
            entity_id=entity_id,
            entity_type=entity_type,
            coordinate=initial_state,
            timestamp=datetime.now(),
            metadata={"reason": "initialization"},
            triggering_event="entity_created"
        )

        self.snapshots[entity_id] = [snapshot]
        self.current_states[entity_id] = initial_state
        return initial_state

    def transition(self, entity_id: str, new_coordinate: StateCoordinate,
                  triggered_by: Optional[str] = None, metadata: Optional[Dict] = None) -> bool:
        """
        Transition entity to a new state.
        Returns True if transition was valid, False otherwise.
        """
        if entity_id not in self.current_states:
            return False

        current = self.current_states[entity_id]

        # Validate decision state transition
        if not self._is_valid_decision_transition(current.decision, new_coordinate.decision):
            return False

        # Validate risk state (can escalate or deescalate)
        # No validation needed - risk can change freely

        # Validate compliance state transition
        if not self._is_valid_compliance_transition(current.compliance, new_coordinate.compliance):
            return False

        # Create snapshot
        snapshot = StateSnapshot(
            entity_id=entity_id,
            entity_type=self.snapshots[entity_id][0].entity_type if entity_id in self.snapshots else "unknown",
            coordinate=new_coordinate,
            timestamp=datetime.now(),
            metadata=metadata or {},
            triggered_by=triggered_by
        )

        # Record transition
        self.snapshots[entity_id].append(snapshot)
        self.current_states[entity_id] = new_coordinate

        return True

    def get_current_state(self, entity_id: str) -> Optional[StateCoordinate]:
        """Get current state coordinate"""
        return self.current_states.get(entity_id)

    def get_state_history(self, entity_id: str) -> List[StateSnapshot]:
        """Get all state snapshots for an entity"""
        return self.snapshots.get(entity_id, [])

    def query_entities_in_state(self, target_state: StateCoordinate) -> List[str]:
        """Find all entities in a specific state"""
        return [
            entity_id for entity_id, state in self.current_states.items()
            if state == target_state
        ]

    def query_entities_in_dimension(self, dimension: str, value_enum) -> List[str]:
        """Query entities by one dimension"""
        return [
            entity_id for entity_id, state in self.current_states.items()
            if (
                (dimension == "decision" and state.decision == value_enum) or
                (dimension == "risk" and state.risk == value_enum) or
                (dimension == "compliance" and state.compliance == value_enum) or
                (dimension == "resource" and state.resource == value_enum) or
                (dimension == "time" and state.time == value_enum)
            )
        ]

    def get_state_transition_count(self, entity_id: str, dimension: str) -> int:
        """Count transitions in a specific dimension"""
        if entity_id not in self.snapshots:
            return 0

        history = self.snapshots[entity_id]
        if len(history) < 2:
            return 0

        count = 0
        for i in range(1, len(history)):
            prev_val = self._get_dimension_value(history[i-1].coordinate, dimension)
            curr_val = self._get_dimension_value(history[i].coordinate, dimension)
            if prev_val != curr_val:
                count += 1

        return count

    def get_state_stability(self, entity_id: str) -> float:
        """
        Get state stability score (0-1).
        Higher = more stable (fewer state changes)
        """
        if entity_id not in self.snapshots:
            return 0.0

        history = self.snapshots[entity_id]
        if len(history) <= 1:
            return 1.0

        # Count state changes
        changes = 0
        for i in range(1, len(history)):
            if history[i].coordinate != history[i-1].coordinate:
                changes += 1

        # Stability = 1 - (changes / max_possible_changes)
        max_changes = len(history) - 1
        if max_changes == 0:
            return 1.0

        return max(0.0, 1.0 - (changes / max_changes))

    def predict_next_state(self, entity_id: str) -> Optional[StateCoordinate]:
        """
        Predict likely next state based on history.
        Uses simple pattern matching - in production would use ML.
        """
        if entity_id not in self.snapshots:
            return None

        history = self.snapshots[entity_id]
        if len(history) < 2:
            return None

        current = self.current_states[entity_id]

        # Based on current state, predict next likely state
        # This is simplified - real prediction would use ML models

        if current.decision == DecisionState.PENDING_APPROVAL:
            # Most likely next: APPROVED (80%) or ROLLED_BACK (20%)
            return StateCoordinate(
                decision=DecisionState.APPROVED,
                risk=current.risk,
                compliance=current.compliance,
                resource=current.resource,
                time=current.time
            )
        elif current.decision == DecisionState.APPROVED:
            return StateCoordinate(
                decision=DecisionState.IN_EXECUTION,
                risk=current.risk,
                compliance=current.compliance,
                resource=current.resource,
                time=current.time
            )
        elif current.decision == DecisionState.IN_EXECUTION:
            return StateCoordinate(
                decision=DecisionState.COMPLETED,
                risk=current.risk,
                compliance=current.compliance,
                resource=current.resource,
                time=current.time
            )

        return None

    def _is_valid_decision_transition(self, current: DecisionState, target: DecisionState) -> bool:
        """Check if decision state transition is valid"""
        return target in self.VALID_TRANSITIONS.get(current, [])

    def _is_valid_compliance_transition(self, current: ComplianceState, target: ComplianceState) -> bool:
        """Check if compliance state transition is valid"""
        # Any transition is allowed for compliance
        return True

    def _get_dimension_value(self, coordinate: StateCoordinate, dimension: str) -> Enum:
        """Get value of a dimension from coordinate"""
        if dimension == "decision":
            return coordinate.decision
        elif dimension == "risk":
            return coordinate.risk
        elif dimension == "compliance":
            return coordinate.compliance
        elif dimension == "resource":
            return coordinate.resource
        elif dimension == "time":
            return coordinate.time
        else:
            return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "current_states": {
                entity_id: state.to_dict()
                for entity_id, state in self.current_states.items()
            },
            "snapshots": {
                entity_id: [
                    {
                        "coordinate": snap.coordinate.to_dict(),
                        "timestamp": snap.timestamp.isoformat(),
                        "metadata": snap.metadata,
                        "triggered_by": snap.triggered_by
                    }
                    for snap in snapshots
                ]
                for entity_id, snapshots in self.snapshots.items()
            }
        }
