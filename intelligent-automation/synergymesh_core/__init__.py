"""
SynergyMesh Core - 無人化自主協同網格系統
Autonomous Coordination Grid System

This module provides the core components for SynergyMesh's revolutionary
fully autonomous system grid that enables:

1. Zero Technical Barrier - Natural language interface
2. Fully Autonomous - 24/7 self-operating capabilities
3. Intelligent Adaptation - Automatic learning and adjustment
4. Ecosystem Coordination - Independent yet coordinated subsystems

設計哲學: 讓程式服務於人類，而非人類服務於程式
"""

from .natural_language_processor import NaturalLanguageProcessor
from .autonomous_coordinator import AutonomousCoordinator
from .self_evolution_engine import SelfEvolutionEngine
from .ecosystem_orchestrator import EcosystemOrchestrator

__all__ = [
    "NaturalLanguageProcessor",
    "AutonomousCoordinator",
    "SelfEvolutionEngine",
    "EcosystemOrchestrator",
]

__version__ = "1.0.0"
