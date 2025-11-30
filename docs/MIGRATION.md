# SynergyMesh Directory Migration Guide

## Overview

This document describes the directory topology migration (Proposal v1) for the SynergyMesh project. The migration reorganizes the repository structure to improve maintainability, clarity, and separation of concerns.

## Migration Summary

### Date
November 2025

### Purpose
- Centralize meta-configuration under `.meta/`
- Better organize platform components under `platform/`
- Separate supply chain artifacts under `supply-chain/`
- Improve infrastructure organization under `infra/`
- Clearer application structure under `app/` and `services/`

## Directory Mapping

### Meta Configuration (`.meta/`)

| New Location | Original Location | Description |
|--------------|-------------------|-------------|
| `.meta/ci/` | `.github/workflows/` | CI/CD workflows and configurations |
| `.meta/github/` | `.github/` | GitHub-specific configurations (CODEOWNERS, templates, etc.) |
| `.meta/github-private/` | `.github-private/` | Private GitHub configurations |
| `.meta/governance/` | `governance/` | Governance policies and schemas |
| `.meta/vscode/` | `.vscode/` | VS Code workspace settings |
| `.meta/devcontainer/` | `.devcontainer/` | Dev container configurations |
| `.meta/policies/` | `governance/policies/conftest/` | Conftest policies (centralized) |
| `.meta/registry/` | `governance/registry/` | Service/module registry |
| `.meta/attest/` | `attest-build-provenance-main/` | Attestation templates and signing policies |

### Supply Chain (`supply-chain/`)

| New Location | Original Location | Description |
|--------------|-------------------|-------------|
| `supply-chain/sbom/` | `governance/sbom/` | SBOM generation and provenance |
| `supply-chain/attestations/` | (new) | SLSA/L3 evidence storage |
| `supply-chain/registry/` | (optional) | Alternative registry location |

### Platform Components (`platform/`)

| New Location | Original Location | Description |
|--------------|-------------------|-------------|
| `platform/core/` | `core/` | Core platform services |
| `platform/runtime/` | `runtime/` | Runtime components |
| `platform/shared/` | `shared/` | Shared utilities and constants |
| `platform/bridges/` | `bridges/` | Language and system bridges |
| `platform/mcp/` | `mcp-servers/` | MCP server implementations |
| `platform/agent/` | `agent/` | Agent services |

### Application Layer (`app/`)

| New Location | Original Location | Description |
|--------------|-------------------|-------------|
| `app/frontend/ui/` | `frontend/ui/` | Frontend UI components |

### Services (`services/`)

| New Location | Original Location | Description |
|--------------|-------------------|-------------|
| `services/contracts/` | `contracts/` | Application layer contracts/ABI |

### Infrastructure (`infra/`)

| New Location | Original Location | Description |
|--------------|-------------------|-------------|
| `infra/infrastructure/` | `infrastructure/` | Infrastructure configurations |
| `infra/config/` | `config/` | System configurations |
| `infra/runtime-profiles/` | (new) | Runtime environment profiles |

### Other Changes

| New Location | Original Location | Description |
|--------------|-------------------|-------------|
| `docker-templates/` | `.docker-templates/` | Docker template files |
| `tests/e2e/` | (new) | End-to-end tests |
| `tests/integration/` | (new) | Integration tests |
| `tests/unit/` | `tests/` | Unit tests |
| `examples/` | (new) | Usage examples |
| `scripts/` | (new) | Migration and generation tools |
| `.config/conftest/` | `governance/policies/conftest/` | Conftest framework (policies in `.meta/policies/`) |

## Migration Steps

### Automated Migration

A migration script is provided at `scripts/migrate-topology.sh` (if available) to automate the directory restructuring.

### Manual Migration

1. Create the new directory structure
2. Copy files to new locations
3. Update import paths in source files
4. Update `package.json` workspace paths
5. Update CI/CD workflow paths
6. Test all builds and tests

## Compatibility Layer

See [BUILD_COMPAT.md](./BUILD_COMPAT.md) for information on maintaining backwards compatibility during the transition period.

## Verification

After migration, verify:

1. All tests pass: `npm test`
2. Build succeeds: `npm run build`
3. Linting passes: `npm run lint`
4. CI/CD workflows function correctly

## Rollback

If issues arise, the original directory structure is preserved. To rollback:

1. Remove new directories
2. The original directories remain intact for reference

## Notes

- Original directories are preserved during transition for reference
- Symbolic links may be used for backwards compatibility
- Update any external references to the repository structure
