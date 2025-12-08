# Governance

# 治理

> 治理政策、規則、安全配置和合規資源。
> Governance policies, rules, security configurations, and compliance resources.

## 📋 Overview 概述

本目錄包含 SynergyMesh 項目的治理配置和文檔，確保模組間的責任清晰、依賴管理合理、語言邊界明確。

This directory contains governance configurations and documentation for the SynergyMesh project, ensuring clear module responsibilities, reasonable dependency management, and explicit language boundaries.

## 🎯 Architecture Governance Matrix | 架構治理矩陣 ⭐

**[📖 Read the Architecture Governance Matrix](./ARCHITECTURE_GOVERNANCE_MATRIX.md)**

The Architecture Governance Matrix is a comprehensive framework that extends beyond simple directory mapping to include **nine governance dimensions**:

架構治理矩陣是一個全面的框架，超越了簡單的目錄映射，包含 **九個治理維度**：

### Core Structural Contracts | 核心結構契約
1. **Namespace** - Logical naming and boundaries
2. **Module Mapping** - Logical ID to physical path mapping
3. **Dependency Rules** - Who can call whom

### Extended Governance Dimensions | 延伸治理維度
4. **Layers & Domains** - Semantic definitions and responsibilities
5. **Roles & Capabilities** - Module behavioral intent
6. **Behavior Contracts** - API, events, invariants, failure modes
7. **Lifecycle & Ownership** - Team ownership and module state
8. **Policies & Constraints** - Executable architectural policies
9. **Quality & Metrics** - Measurable architecture health

This matrix makes architecture governance **explicit, measurable, and automatable**.

## 📁 Directory Structure 目錄結構

```
governance/
├── ARCHITECTURE_GOVERNANCE_MATRIX.md  # 🎯 架構治理矩陣（核心文檔）
├── architecture/                      # 架構定義
│   └── layers-domains.yaml           # 層級與領域語義定義
├── behavior-contracts/                # 行為契約
│   ├── README.md                     # 契約指南
│   └── *.yaml                        # 各模組的行為契約
├── modules/                           # 模組角色與能力
│   ├── README.md                     # 模組規範指南
│   └── *.yaml                        # 各模組的詳細規範
├── ownership-map.yaml                 # 所有權與生命週期映射
├── architecture-health.yaml           # 架構健康度指標
├── policies/                          # 策略定義
│   ├── architecture-rules.yaml       # 架構策略規則
│   └── ...                           # 其他策略
├── audit/                             # 審計配置
├── deployment/                        # 部署配置
├── environment-matrix/                # 模組環境映射
├── registry/                          # 模組治理註冊表
├── rules/                             # 治理規則
├── sbom/                              # 軟體物料清單
└── schemas/                           # Schema 定義
```

## 🎯 What This Directory Does 本目錄負責什麼

### ✅ Responsibilities 職責

1. **Policy Definitions 策略定義** (`policies/`)
   - 安全策略
   - 存取控制策略
   - 代碼品質策略
   - Conftest/OPA 策略

2. **Audit Configurations 審計配置** (`audit/`)
   - 審計日誌配置
   - 合規檢查規則
   - 審計報告模板

3. **Governance Rules 治理規則** (`rules/`)
   - 依賴管理規則
   - 版本控制規則
   - 發布流程規則

4. **Software Bill of Materials 軟體物料清單** (`sbom/`)
   - 依賴清單
   - 授權資訊
   - 簽章策略

5. **Schema Definitions Schema 定義** (`schemas/`)
   - 配置文件 schema
   - API schema
   - Data model definitions / 資料模型定義

6. **Environment Matrix 環境映射** (`environment-matrix/`)
   - 模組環境需求映射
   - 語言維度映射
   - 條件式部署配置

7. **Deployment Configuration 部署配置** (`deployment/`)
   - 服務部署配置
   - Kubernetes 清單

8. **Module Registry 模組註冊表** (`registry/`)
   - 服務治理元數據
   - 模組依賴關係

### ❌ What This Directory Does NOT Do 本目錄不負責什麼

- **No executable code** - Except validation scripts / 除驗證腳本外
- **No business logic** - Only policy and rule definitions / 僅政策和規則定義
- **No runtime configuration** - Use `config/` instead / 使用 `config/`

## 🔗 Dependencies 依賴關係

### ✅ Who Should Depend on This 誰應該依賴本目錄

| Consumer 使用者 | Purpose 用途 |
|----------------|--------------|
| CI/CD workflows | Policy validation and compliance checks / 策略驗證和合規檢查 |
| `core/` | 讀取 AI 憲法和倫理規則 |
| Security tools | SBOM 和安全策略 |

### ❌ This Directory Should NOT Depend on 本目錄不應依賴

| 不應依賴 | Reason 原因 |
|---------|-------------|
| 任何實作代碼 | 治理應獨立於實作 |
| `runtime/` | 治理定義不應依賴運行時 |

## 📖 Related Documentation 相關文檔

- [Architecture Layers](../docs/architecture/layers.md) - 架構分層視圖
- [Repository Map](../docs/architecture/repo-map.md) - 倉庫語義邊界
- [Security Training](../docs/SECURITY_TRAINING.md) - 安全培訓
- [Vulnerability Management](../docs/VULNERABILITY_MANAGEMENT.md) - 漏洞管理

## 📝 Document History 文檔歷史

| Date 日期 | Version 版本 | Changes 變更 |
|-----------|-------------|--------------|
| 2025-11-30 | 1.0.0 | Initial README |

---

**Owner 負責人**: Governance Team  
**Last Updated 最後更新**: 2025-11-30

# Supply Chain Directory

This directory contains supply chain security artifacts for SynergyMesh.

## Structure

```
supply-chain/
├── sbom/          # Software Bill of Materials
├── attestations/  # SLSA/L3 evidence
└── registry/      # Component registry (optional)
```

## Components

### SBOM (`sbom/`)

Software Bill of Materials containing:

- SPDX format SBOMs
- Provenance information
- Signing policies

### Attestations (`attestations/`)

SLSA Level 3 attestation evidence:

- Build attestations
- Provenance records
- Verification artifacts

### Registry (`registry/`)

Optional component registry for:

- Module versions
- Service definitions
- Contract schemas

## SLSA Compliance

SynergyMesh follows SLSA (Supply-chain Levels for Software Artifacts) framework:

- Level 1: Documentation of build process
- Level 2: Tamper resistance through hosted build
- Level 3: Security against specific threats

## See Also

- [SLSA Framework](https://slsa.dev/)
- [Migration Guide](../docs/MIGRATION.md)
- [Sigstore Documentation](https://docs.sigstore.dev/)
