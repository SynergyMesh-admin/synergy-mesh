# Refactor Playbook: governance/

**Generated:** 2025-12-10T00:58:26.997060  
**Cluster Score:** 55  
**Status:** Draft (LLM generation required for complete playbook)

---

## 1. Cluster 概覽

**Cluster Path:** `governance/`  
**Current Status:** 需要重構與語言治理改進

這個 cluster 在 Unmanned Island System 中的角色：
- 路徑位置：governance/
- 違規數量：0
- Hotspot 檔案：1
- 安全問題：0

---

## 2. 問題盤點

### 語言治理違規 (0)

✅ 無語言治理違規

### Hotspot 檔案 (1)

- **governance/audit/checker.rb** (score: 55)

### Semgrep 安全問題 (0)

✅ 無安全問題


---

## 3. 語言與結構重構策略

**注意：** 此部分需要使用 LLM 生成完整建議。

預期內容：
- 語言層級策略（保留/遷出語言）
- 目錄結構優化建議
- 語言遷移路徑

---

## 4. 分級重構計畫（P0 / P1 / P2）

**注意：** 此部分需要使用 LLM 生成具體行動計畫。

### P0（24–48 小時內必須處理）
- 待 LLM 生成

### P1（一週內）
- 待 LLM 生成

### P2（持續重構）
- 待 LLM 生成

---

## 5. 適合交給 Auto-Fix Bot 的項目

**可自動修復：**
- 待 LLM 分析

**需人工審查：**
- 待 LLM 分析

---

## 6. 驗收條件與成功指標

**語言治理目標：**
- 違規數 < 5
- 安全問題 HIGH severity = 0
- Cluster score < 20

**改善方向：**
- 待 LLM 生成具體建議

---

## 7. 檔案與目錄結構（交付視圖）

### 受影響目錄

- governance/

### 結構示意（變更範圍）

```
governance/
├── _scratch/
│   ├── .gitkeep
│   └── README.md
├── api-governance/
│   ├── config/
│   │   └── api-policy.yaml
│   ├── schemas/
│   │   └── api-schema.json
│   └── README.md
├── architecture/
│   ├── README.md
│   └── layers-domains.yaml
├── architecture-governance/
│   ├── config/
│   │   └── architecture-policy.yaml
│   ├── schemas/
│   │   └── architecture-schema.json
│   └── README.md
├── audit/
│   ├── append-only-log-client.js
│   └── format.yaml
├── audit-governance/
│   ├── AUTOMATION_ENGINE_README.md
│   ├── README.md
│   ├── __init__.py
│   ├── audit-framework.yaml
│   ├── audit-plan-annual.yaml
│   └── automation_engine.py
├── automation/
│   ├── coordinator/
│   │   ├── __init__.py
│   │   └── engine_coordinator.py
│   ├── engines/
│   │   ├── __init__.py
│   │   └── dimension_automation_engine.py
│   ├── README.md
│   ├── SYSTEM_OVERVIEW.md
│   ├── __init__.py
│   ├── deploy_dimension_engines.py
│   ├── governance_automation_launcher.py
│   ├── integrated_launcher.py
│   └── test_automation_system.py
├── behavior-contracts/
│   ├── README.md
│   ├── apps.web.ui.yaml
│   ├── automation.architect.yaml
│   ├── automation.autonomous.yaml
│   ├── automation.hyperautomation.yaml
│   ├── automation.intelligent.yaml
│   ├── core.contract_service.L1.yaml
│   ├── core.mind_matrix.yaml
│   ├── core.safety_mechanisms.yaml
│   ├── core.slsa_provenance.yaml
│   ├── core.unified_integration.yaml
│   ├── island_ai.yaml
│   └── services.mcp.yaml
├── change-governance/
│   ├── AUTOMATION_ENGINE_README.md
│   ├── README.md
│   ├── __init__.py
│   ├── automation_engine.py
│   ├── change-classification.yaml
│   ├── change-control-matrix.yaml
│   └── change-processes.yaml
├── common/
│   ├── schemas/
│   │   ├── config.schema.json
│   │   ├── dependency.schema.json
│   │   ├── framework.schema.json
│   │   └── policy.schema.json
│   ├── tools/
│   │   ├── dependency_analyzer.py
│   │   ├── governance_policy_checker.py
│   │   ├── schema_validator.py
│   │   └── validate_governance_matrix.py
│   └── README.md
├── compliance-governance/
│   ├── AUTOMATION_ENGINE_README.md
│   ├── README.md
│   ├── __init__.py
│   ├── automation_engine.py
│   ├── compliance-check-rules.yaml
│   └── compliance-standards.yaml
├── cost-management-governance/
│   ├── config/
│   │   └── cost-policy.yaml
│   ├── schemas/
│   │   └── cost-schema.json
│   └── README.md
├── data-governance/
│   ├── config/
│   │   └── data-policy.yaml
│   ├── schemas/
│   │   └── data-schema.json
│   └── README.md
├── decision-governance/
│   ├── AUTOMATION_ENGINE_README.md
│   ├── README.md
│   ├── __init__.py
│   ├── automation_engine.py
│   ├── decision-authority-matrix.yaml
│   ├── decision-framework.yaml
│   └── decision-processes.yaml
├── deployment/
│   └── matechat-services.yml
├── docs-governance/
│   ├── config/
│   │   └── docs-policy.yaml
│   └── README.md
├── environment-matrix/
│   ├── LANGUAGE_DIMENSION_MAPPING.md
│   └── module-environment-matrix.yml
├── governance-architecture/
│   ├── AUTOMATION_ENGINE_README.md
│   ├── README.md
│   ├── __init__.py
│   ├── automation_engine.py
│   ├── governance-model.yaml
│   ├── governance-principles.yaml
│   └── organizational-structure.yaml
├── governance-culture/
│   ├── AUTOMATION_ENGINE_README.md
│   ├── README.md
│   ├── __init__.py
│   ├── automation_engine.py
│   ├── capability-model.yaml
│   └── governance-values.yaml
├── governance-improvement/
│   ├── AUTOMATION_ENGINE_README.md
│   ├── README.md
│   ├── __init__.py
│   ├── automation_engine.py
│   ├── improvement-identification.yaml
│   └── improvement-planning.yaml
└── ... (36 more items)
```

### 檔案說明

- `governance/README.md` — 說明文檔
- `governance/policies/conftest/matechat-integration/README.md` — 說明文檔
- `governance/architecture-governance/README.md` — 說明文檔
- `governance/governance-tools/README.md` — 說明文檔
- `governance/governance-tools/__init__.py` — Python 套件初始化
- `governance/performance-governance/README.md` — 說明文檔
- `governance/performance-governance/__init__.py` — Python 套件初始化
- `governance/audit-governance/README.md` — 說明文檔
- `governance/audit-governance/__init__.py` — Python 套件初始化
- `governance/testing-governance/README.md` — 說明文檔

---

## 如何使用本 Playbook

1. **立即執行 P0 項目**：處理高優先級問題
2. **規劃 P1 重構**：安排一週內執行
3. **持續改進**：納入 P2 到長期技術債計畫
4. **交給 Auto-Fix Bot**：自動化可修復項目
5. **人工審查**：關鍵架構調整需要工程師參與

