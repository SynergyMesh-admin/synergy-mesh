# Governance
# 治理

> 治理政策、規則、安全配置和合規資源。
> Governance policies, rules, security configurations, and compliance resources.

## 📋 Overview 概述

本目錄包含 SynergyMesh 平台的治理資源，包括策略定義、審計配置、軟體物料清單 (SBOM) 和 schema 定義。

This directory contains governance resources for the SynergyMesh platform, including policy definitions, audit configurations, software bill of materials (SBOM), and schema definitions.

## 📁 Directory Structure 目錄結構

```
governance/
├── audit/       # 審計配置 - Audit configurations
├── policies/    # 策略定義 - Policy definitions
├── rules/       # 治理規則 - Governance rules
├── sbom/        # 軟體物料清單 - Software Bill of Materials
└── schemas/     # Schema 定義 - Schema definitions
```

## 🎯 What This Directory Does 本目錄負責什麼

### ✅ Responsibilities 職責

1. **Policy Definitions 策略定義** (`policies/`)
   - 安全策略
   - 存取控制策略
   - 代碼品質策略

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
