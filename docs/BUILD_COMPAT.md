# Build Compatibility Guide

## Overview

This document explains the compatibility layer maintained during the directory topology migration to ensure existing builds, tests, and CI/CD pipelines continue to function.

## Workspace Configuration

### Original Workspaces

The original `package.json` workspaces configuration:

```json
{
  "workspaces": [
    "mcp-servers",
    "core/contract_service/contracts-L1/contracts",
    "core/advisory-database",
    "frontend/ui"
  ]
}
```

### New Workspaces (Post-Migration)

```json
{
  "workspaces": [
    "platform/mcp",
    "platform/core/contract_service/contracts-L1/contracts",
    "platform/core/advisory-database",
    "app/frontend/ui"
  ]
}
```

## Transition Strategy

During the transition period, both directory structures are maintained:

1. **Original directories** - Remain in place for backwards compatibility
2. **New directories** - Contain the migrated structure

## Path Aliases

Consider adding path aliases in `tsconfig.json` for smoother transition:

```json
{
  "compilerOptions": {
    "paths": {
      "@platform/*": ["platform/*"],
      "@app/*": ["app/*"],
      "@services/*": ["services/*"],
      "@infra/*": ["infra/*"],
      "@meta/*": [".meta/*"]
    }
  }
}
```

## CI/CD Updates

### GitHub Actions Workflow Paths

Update workflow triggers to use new paths:

```yaml
# Before
on:
  push:
    paths:
      - 'core/**'
      - 'mcp-servers/**'

# After (transition period - both)
on:
  push:
    paths:
      - 'core/**'
      - 'mcp-servers/**'
      - 'platform/**'

# After (complete migration)
on:
  push:
    paths:
      - 'platform/**'
```

## Import Path Updates

### TypeScript/JavaScript Imports

When migrating imports, update paths gradually:

```typescript
// Before
import { something } from '../../core/services/some-service';

// After
import { something } from '@platform/core/services/some-service';
```

## Testing

### Ensuring Test Compatibility

1. Run tests from both old and new locations
2. Verify all test fixtures are accessible
3. Update test configuration paths as needed

### Jest Configuration

Update `jest.config.js` roots if needed:

```javascript
module.exports = {
  roots: [
    '<rootDir>/platform',
    '<rootDir>/app',
    '<rootDir>/tests'
  ],
  // ... other config
};
```

## Build Scripts

### NPM Scripts

Ensure build scripts work with new structure:

```json
{
  "scripts": {
    "build": "npm run build --workspaces --if-present",
    "test": "npm run test --workspaces --if-present",
    "lint": "npm run lint --workspaces --if-present"
  }
}
```

## Docker Build Context

Update Dockerfile paths if needed:

```dockerfile
# Update COPY commands
COPY platform/core ./platform/core
COPY app/frontend ./app/frontend
```

## Known Issues

1. **Symlinks**: Some environments may have issues with symlinks
2. **IDE indexing**: IDEs may need to re-index after migration
3. **Cache invalidation**: Clear build caches after migration

## Deprecation Timeline

1. **Phase 1**: Both structures exist (current)
2. **Phase 2**: Warnings for old paths (future)
3. **Phase 3**: Old structure removed (future)

## Support

For migration issues, refer to:
- [MIGRATION.md](./MIGRATION.md) - Full migration guide
- [docs/architecture/](./architecture/) - Architecture documentation
