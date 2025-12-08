# Architecture Definitions
# 架構定義

> **Purpose**: Define architectural layers, domains, and their semantic meanings  
> **用途**: 定義架構層級、領域及其語義含義

## 📋 Overview | 概述

This directory contains architectural definitions that give semantic meaning to the system's structure. These definitions go beyond simple naming conventions to establish clear responsibilities, boundaries, and relationships.

本目錄包含架構定義，為系統結構賦予語義含義。這些定義超越了簡單的命名約定，建立了清晰的責任、邊界和關係。

## 📄 Files | 檔案

### layers-domains.yaml

**[📖 View layers-domains.yaml](./layers-domains.yaml)**

The comprehensive definition of:

1. **Architectural Layers** (7 layers)
   - Infrastructure
   - Governance
   - Runtime
   - Core
   - Automation
   - Services
   - Apps

2. **Functional Domains** (6+ domains)
   - Contract management
   - Autonomous systems
   - Security & compliance
   - Language governance
   - Monitoring & observability
   - Billing & financial

3. **Layer-Domain Matrix**
   - Valid combinations
   - Integration patterns
   - Cross-domain interfaces

## 🎯 What This Defines | 定義內容

### For Each Layer | 每個層級定義

- **Order**: Vertical position in hierarchy (1-7)
- **Description**: What the layer does
- **Responsibilities**: Clear scope of work
- **Restrictions**: What it cannot do
- **Dependencies**: Allowed and prohibited dependencies
- **Languages**: Permitted programming languages
- **Examples**: Real modules in this layer

### For Each Domain | 每個領域定義

- **Description**: Domain purpose and scope
- **Capabilities**: What the domain provides
- **Modules**: Which modules belong to this domain
- **Owner**: Responsible team
- **Cross-domain interfaces**: How domains interact

## 🔗 How It's Used | 使用方式

### By Developers

```bash
# Check if a dependency is allowed
# Example: Can services depend on apps?
cat layers-domains.yaml | yq '.layers.services.dependencies.prohibited'
# Output: ["apps"]
# Answer: No, prohibited

# Check allowed languages for a layer
cat layers-domains.yaml | yq '.layers.core.allowed_languages'
# Output: ["python", "typescript", "go"]
```

### By CI/CD

- Validate layer dependencies in PRs
- Check language policy compliance
- Enforce architectural boundaries
- Generate architecture reports

### By AI Agents

- Understand system structure semantically
- Make architecture-aware decisions
- Suggest appropriate layer for new code
- Detect architectural violations

## ✅ Validation Rules | 驗證規則

Defined in the file:

1. **Layer Dependency Check**: Verify dependency hierarchy
2. **Domain Isolation Check**: Ensure proper interfaces
3. **Language Policy Check**: Validate language usage
4. **Circular Dependency Check**: Detect cycles

These are enforced by:
- CI pipeline checks
- Architecture review process
- Automated validation scripts

## 🔄 Evolution Strategy | 演化策略

### Principles | 原則

- **Layers are stable**: Architectural invariants
- **Domains can evolve**: Business needs change
- **Breaking changes need process**: Migration path required
- **Additive changes preferred**: Don't break existing code

### Deprecation Process | 棄用流程

When deprecating a layer or domain:

1. Mark as deprecated in this file
2. Update ownership-map.yaml with migration path
3. Provide 2 release cycles notice
4. Document migration in behavior-contracts/
5. Remove in next major version

## 📊 Example Queries | 範例查詢

### Can Module A Depend on Module B?

1. Find module A's layer
2. Find module B's layer
3. Check A's layer `dependencies.allowed`
4. Check if B's layer is in the list

### What Language Can I Use in Layer X?

1. Find layer X in `layers`
2. Check `allowed_languages`
3. Check `globally_prohibited` for exceptions

### Which Modules Belong to Domain Y?

1. Find domain Y in `domains`
2. Check the `modules` list
3. Each entry is a namespace ID

## 🔗 Related Files | 相關檔案

- [Architecture Governance Matrix](../ARCHITECTURE_GOVERNANCE_MATRIX.md) - Overall framework
- [Module Mapping](../../config/system-module-map.yaml) - Physical paths
- [Ownership Map](../ownership-map.yaml) - Teams and lifecycle
- [Architecture Policies](../policies/architecture-rules.yaml) - Executable rules

## 📝 Editing Guidelines | 編輯指南

When modifying `layers-domains.yaml`:

1. **Think carefully**: These are architectural invariants
2. **Get approval**: Requires architecture team review
3. **Document changes**: Update this README if structure changes
4. **Update references**: Many files reference these definitions
5. **Test validation**: Run `make validate-governance`
6. **Communicate**: Announce architectural changes

## 🎓 Learning Path | 學習路徑

### For New Team Members

1. Read this README
2. Study `layers-domains.yaml` structure
3. Review examples in each layer
4. Understand your domain's boundaries
5. Check cross-domain interfaces you'll use

### For Architects

1. Understand the complete layer hierarchy
2. Know all domain interactions
3. Review validation rules
4. Plan evolution strategy
5. Guide team on architectural decisions

---

**Owner**: Architecture Team  
**Last Updated**: 2025-12-07  
**Review Frequency**: Quarterly
