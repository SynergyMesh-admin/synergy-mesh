"""
Phase 22: Unified System Integration

This module provides the unified integration layer that connects all SynergyMesh
components into a cohesive, production-ready system. It bridges phases 1-21 into
a seamless operational framework.

Key Components:
- UnifiedSystemController: Central orchestration for all phases
- IntegrationHub: Cross-phase communication and coordination
- SystemOrchestrator: High-level system management
- ConfigurationManager: Unified configuration management
"""

from .unified_controller import UnifiedSystemController
from .integration_hub import IntegrationHub, IntegrationConfig
from .system_orchestrator import SystemOrchestrator, OrchestratorConfig
from .configuration_manager import ConfigurationManager, SystemConfiguration

__all__ = [
    'UnifiedSystemController',
    'IntegrationHub',
    'IntegrationConfig',
    'SystemOrchestrator',
    'OrchestratorConfig',
    'ConfigurationManager',
    'SystemConfiguration',
]

__version__ = '1.0.0'
__author__ = 'SynergyMesh Team'
