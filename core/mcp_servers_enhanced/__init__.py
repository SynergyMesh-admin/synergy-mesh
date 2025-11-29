"""
Phase 19: MCP Servers Enhanced Integration Module

This module provides enhanced MCP (Model Context Protocol) server integrations
with real tool definitions, workflow orchestration, and advanced capabilities.

Key Components:
- MCPServerManager: Central manager for all MCP servers
- ToolRegistry: Registry for available tools across all servers
- WorkflowOrchestrator: Orchestrates complex multi-tool workflows
- RealTimeConnector: Real-time connection management for MCP servers
"""

from .mcp_server_manager import MCPServerManager, MCPServer, MCPServerConfig
from .tool_registry import ToolRegistry, ToolDefinition, ToolExecutionResult
from .workflow_orchestrator import WorkflowOrchestrator, WorkflowStep, WorkflowResult
from .realtime_connector import RealTimeConnector, ConnectionStatus, ConnectionConfig

__all__ = [
    'MCPServerManager',
    'MCPServer',
    'MCPServerConfig',
    'ToolRegistry',
    'ToolDefinition',
    'ToolExecutionResult',
    'WorkflowOrchestrator',
    'WorkflowStep',
    'WorkflowResult',
    'RealTimeConnector',
    'ConnectionStatus',
    'ConnectionConfig',
]

__version__ = '1.0.0'
__author__ = 'SynergyMesh Team'
