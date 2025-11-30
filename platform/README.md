# Platform Directory

This directory contains the core platform components of SynergyMesh.

## Structure

```
platform/
├── core/      # Core platform services
├── runtime/   # Runtime components
├── shared/    # Shared utilities and constants
├── bridges/   # Language and system bridges
├── mcp/       # MCP server implementations
└── agent/     # Agent services
```

## Components

### Core (`core/`)
Contains the main platform services including:
- Contract service
- Advisory database
- AI decision engine
- Safety mechanisms
- SLSA provenance

### Runtime (`runtime/`)
Runtime components and mind matrix implementation.

### Shared (`shared/`)
Shared utilities, constants, and configurations used across the platform.

### Bridges (`bridges/`)
Language bridges for cross-language communication.

### MCP (`mcp/`)
Model Context Protocol server implementations.

### Agent (`agent/`)
Agent services including:
- Auto-repair
- Code analyzer
- Dependency manager
- Orchestrator
- Vulnerability detector

## See Also

- [Migration Guide](../docs/MIGRATION.md)
- [Architecture Documentation](../docs/architecture/)
