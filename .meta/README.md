# .meta Directory

This directory contains meta-configuration files for the SynergyMesh project.

## Structure

```
.meta/
├── ci/              # CI/CD workflows and configurations
├── github/          # GitHub-specific configurations
├── github-private/  # Private GitHub configurations
├── governance/      # Governance policies and schemas
├── vscode/          # VS Code workspace settings
├── devcontainer/    # Dev container configurations
├── policies/        # Conftest policies (centralized)
├── registry/        # Service/module registry
└── attest/          # Attestation templates and signing policies
```

## Usage

These configurations are referenced by various tools and services:

- **CI workflows** are symlinked to `.github/workflows/` for GitHub Actions
- **VS Code settings** can be symlinked to `.vscode/` for IDE support
- **DevContainer** config is symlinked to `.devcontainer/` for container development

## See Also

- [Migration Guide](../docs/MIGRATION.md)
- [Build Compatibility](../docs/BUILD_COMPAT.md)
