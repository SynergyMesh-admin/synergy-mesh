#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Causal Inference Engine

Provides forward/backward inference, intervention analysis, and counterfactual reasoning
on governance causal graphs.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass
import math


@dataclass
class InferenceResult:
    """Result of a causal inference query"""
    query_type: str              # "forward", "backward", "intervention", "counterfactual"
    source_variable: str
    target_variable: str
    inferred_value: Optional[str]
    probability: float           # Confidence (0-1)
    reasoning_chain: List[str]   # Explanation of reasoning
    affected_variables: List[str] # Other variables affected
    confidence_score: float      # Overall confidence


class CausalInferenceEngine:
    """Performs causal inference on governance graphs"""

    def __init__(self, causal_graph):
        """Initialize with a causal graph"""
        self.graph = causal_graph
        self._belief_cache: Dict[str, Dict[str, float]] = {}

    def forward_inference(self, source_var: str, source_value: str) -> InferenceResult:
        """
        Forward inference: Given a cause, what are the likely effects?

        Example:
        - If "decision-to-accelerate-change" = True
        - Then what's the probability of "increase-in-errors"?
        """
        if source_var not in self.graph.nodes:
            raise ValueError(f"Variable {source_var} not found in graph")

        # Set the source variable
        self.graph.nodes[source_var].current_value = source_value

        # Find all descendants and compute belief propagation
        descendants = self.graph.get_descendants(source_var)
        affected_beliefs: Dict[str, Dict[str, float]] = {}

        for descendant in descendants:
            # Compute probability for each possible value
            affected_beliefs[descendant] = self._compute_belief(descendant, source_var, source_value)

        # Determine most likely effect
        max_prob_var = max(affected_beliefs.keys(), key=lambda v: max(affected_beliefs[v].values()), default=None)
        max_prob_value = max(affected_beliefs[max_prob_var].keys(), key=affected_beliefs[max_prob_var].get) if max_prob_var else None
        max_prob = affected_beliefs[max_prob_var][max_prob_value] if max_prob_var else 0

        reasoning_chain = self._explain_forward_reasoning(source_var, source_value, max_prob_var)

        return InferenceResult(
            query_type="forward",
            source_variable=source_var,
            target_variable=max_prob_var,
            inferred_value=max_prob_value,
            probability=max_prob,
            reasoning_chain=reasoning_chain,
            affected_variables=list(descendants),
            confidence_score=max_prob
        )

    def backward_inference(self, target_var: str, target_value: str) -> InferenceResult:
        """
        Backward inference: Given an observed effect, what caused it?

        Example:
        - If we observe "high-error-rate" = True
        - What's the likely cause?
        """
        if target_var not in self.graph.nodes:
            raise ValueError(f"Variable {target_var} not found in graph")

        # Find all ancestors that could have caused this
        ancestors = self.graph.get_ancestors(target_var)

        # For each ancestor, compute probability of being the cause
        ancestor_probabilities: Dict[str, float] = {}

        for ancestor in ancestors:
            # Compute likelihood that this ancestor caused the target
            paths = self.graph.find_all_paths(ancestor, target_var)
            if paths:
                # Average likelihood over all paths
                path_likelihoods = [self._path_likelihood(path) for path in paths]
                ancestor_probabilities[ancestor] = sum(path_likelihoods) / len(path_likelihoods)

        # Find most likely cause
        if ancestor_probabilities:
            likely_cause = max(ancestor_probabilities.keys(), key=ancestor_probabilities.get)
            cause_prob = ancestor_probabilities[likely_cause]
        else:
            likely_cause = None
            cause_prob = 0

        reasoning_chain = self._explain_backward_reasoning(likely_cause, target_var, target_value)

        return InferenceResult(
            query_type="backward",
            source_variable=likely_cause,
            target_variable=target_var,
            inferred_value=target_value,
            probability=cause_prob,
            reasoning_chain=reasoning_chain,
            affected_variables=list(ancestors),
            confidence_score=cause_prob
        )

    def intervention_analysis(self, variable: str, intervention: str) -> InferenceResult:
        """
        Intervention analysis: If we intervene on a variable, what happens?

        Example:
        - If we intervene on "approval-level" and change it from "1" to "2"
        - What's the impact on "decision-time" and "success-rate"?
        """
        if variable not in self.graph.nodes:
            raise ValueError(f"Variable {variable} not found in graph")

        # Get current value
        current_value = self.graph.nodes[variable].current_value

        # Simulate intervention
        self.graph.nodes[variable].current_value = intervention

        # Compute effects on all descendants
        descendants = self.graph.get_descendants(variable)
        effects: Dict[str, str] = {}

        for descendant in descendants:
            # Compute new belief for this descendant
            new_belief = self._compute_belief(descendant, variable, intervention)
            likely_value = max(new_belief.keys(), key=new_belief.get)
            effects[descendant] = likely_value

        # Restore original value
        self.graph.nodes[variable].current_value = current_value

        # Determine primary impact
        primary_impact = list(effects.keys())[0] if effects else None
        impact_value = effects.get(primary_impact)

        reasoning_chain = self._explain_intervention(variable, intervention, primary_impact, impact_value)

        return InferenceResult(
            query_type="intervention",
            source_variable=variable,
            target_variable=primary_impact,
            inferred_value=impact_value,
            probability=0.85,  # Simplified
            reasoning_chain=reasoning_chain,
            affected_variables=list(descendants),
            confidence_score=0.85
        )

    def counterfactual_analysis(self, decision_var: str, actual_value: str, alternative_value: str) -> Tuple[InferenceResult, InferenceResult]:
        """
        Counterfactual analysis: Compare outcomes of two different decisions.

        Returns both the actual outcome and the counterfactual outcome.

        Example:
        - Actual: We decided to "slow-down-changes" and got "low-error-rate"
        - Counterfactual: What if we had "speed-up-changes" instead?
        """
        # Analyze actual scenario
        self.graph.nodes[decision_var].current_value = actual_value
        actual_result = self.forward_inference(decision_var, actual_value)

        # Analyze counterfactual scenario
        self.graph.nodes[decision_var].current_value = alternative_value
        counterfactual_result = self.forward_inference(decision_var, alternative_value)

        # Add comparison to reasoning
        counterfactual_result.reasoning_chain.insert(0, f"COUNTERFACTUAL: If we had chosen '{alternative_value}' instead of '{actual_value}'")

        return actual_result, counterfactual_result

    def _compute_belief(self, variable: str, evidence_var: str, evidence_value: str) -> Dict[str, float]:
        """
        Compute belief distribution for a variable given evidence.
        Uses simplified belief propagation.
        """
        if variable not in self.graph.nodes:
            return {}

        node = self.graph.nodes[variable]
        beliefs: Dict[str, float] = {}

        # Get edges connecting evidence to this variable
        relevant_edges = [e for e in self.graph.edges if e.source == evidence_var and self._can_reach(e.target, variable)]

        if not relevant_edges:
            # No connection, use prior probability
            for value in node.possible_values:
                beliefs[value] = 1.0 / len(node.possible_values)
            return beliefs

        # Compute likelihood based on edge strengths and confidence
        total_strength = 0
        for value in node.possible_values:
            likelihood = 0
            for edge in relevant_edges:
                if self._matches_pathway(edge, variable, value):
                    likelihood += edge.strength * edge.confidence
            beliefs[value] = likelihood
            total_strength += likelihood

        # Normalize to probabilities
        if total_strength > 0:
            beliefs = {v: p / total_strength for v, p in beliefs.items()}
        else:
            # Fallback to uniform
            for value in node.possible_values:
                beliefs[value] = 1.0 / len(node.possible_values)

        return beliefs

    def _can_reach(self, from_node: str, to_node: str) -> bool:
        """Check if there's a path from one node to another"""
        return self.graph.find_path(from_node, to_node) is not None

    def _matches_pathway(self, edge, target_var: str, target_value: str) -> bool:
        """Simplified check if edge matches a pathway to target value"""
        # In a full implementation, this would use sophisticated matching
        return edge.target == target_var

    def _path_likelihood(self, path: List[str]) -> float:
        """Compute likelihood of a causal path"""
        likelihood = 1.0
        for i in range(len(path) - 1):
            source = path[i]
            target = path[i + 1]
            # Find edge
            for edge in self.graph.edges:
                if edge.source == source and edge.target == target:
                    likelihood *= edge.strength * edge.confidence
                    break
        return min(likelihood, 1.0)  # Cap at 1.0

    def _explain_forward_reasoning(self, source: str, source_value: str, target: str) -> List[str]:
        """Generate explanation for forward inference"""
        return [
            f"Given: {source} = {source_value}",
            f"Finding: Likely effects through causal pathways",
            f"Result: {target} is most likely affected",
            f"Reasoning: Variable {source} causally influences {target}"
        ]

    def _explain_backward_reasoning(self, cause: str, target: str, target_value: str) -> List[str]:
        """Generate explanation for backward inference"""
        if cause is None:
            return [
                f"Observed: {target} = {target_value}",
                f"Finding: Causal origins",
                f"Result: No clear causal origin found (may be external shock)"
            ]
        return [
            f"Observed: {target} = {target_value}",
            f"Finding: Causal origins",
            f"Result: {cause} is most likely cause",
            f"Reasoning: Backward tracing through causal graph"
        ]

    def _explain_intervention(self, variable: str, intervention: str, affected: str, result_value: str) -> List[str]:
        """Generate explanation for intervention"""
        return [
            f"Intervention: Changing {variable} to {intervention}",
            f"Finding: Effects on dependent variables",
            f"Result: {affected} would likely be {result_value}",
            f"Reasoning: Forward propagation through causal graph"
        ]

    def clear_cache(self) -> None:
        """Clear belief cache"""
        self._belief_cache.clear()
