# Governance Documentation
# 治理文檔

## 概述 Overview

本目錄包含 SynergyMesh 項目的治理配置和文檔，確保模組間的責任清晰、依賴管理合理、語言邊界明確。

This directory contains governance configurations and documentation for the SynergyMesh project, ensuring clear module responsibilities, reasonable dependency management, and explicit language boundaries.

---

## 📁 文件結構 File Structure

```
.governance/
├── README.md                          # 本文件
├── module-environment-matrix.yml      # 模組環境需求映射
└── LANGUAGE_DIMENSION_MAPPING.md      # 語言維度映射文檔
```

---

## 🎯 核心治理原則 Core Governance Principles

### 1. 避免硬編碼依賴 Avoid Hardcoded Dependencies

**問題 Problem:**
```yaml
# ❌ 所有項目強制使用相同依賴
environment:
  python: "3.10"
  requires:
    - ModelScope API
    - camel-ai
```

**解決方案 Solution:**
```yaml
# ✅ 每個模組獨立定義需求
modules:
  intelligent-automation:
    runtime: "python >= 3.8"  # 靈活版本
    optional_dependencies:
      - ModelScope API        # 標記可選
```

### 2. 環境差異化管理 Environment Differentiation

不同模組有不同的語言和運行時需求：

| 模組 | 語言 | 運行時 | 依賴管理 |
|------|------|--------|---------|
| `core/` | TypeScript | Node.js >= 18 | npm |
| `intelligent-automation/` | Python | Python >= 3.8 | pip (可選) |
| `mcp-servers/` | TypeScript | Node.js >= 18 | npm |
| `scripts/` | Shell/Python | 混合 | 條件式 |

### 3. 條件式部署 Conditional Deployment

使用 `scripts/conditional-deploy.sh` 實現智能部署：

```bash
# 自動檢測模組類型
if check_module_requirement "$module" "python"; then
    install_python_deps "$module"
fi

if check_module_requirement "$module" "nodejs"; then
    install_nodejs_deps "$module"
fi
```

### 4. 語言邊界強制 Language Boundary Enforcement

**內部 Internal:**
- 代碼註解：繁體中文
- 內部文檔：繁體中文
- 錯誤訊息：雙語（中文優先）

**外部 External:**
- 公開 API：雙語（中文 + 英文）
- 第三方集成：英文
- 開源發佈：雙語

---

## 📊 六大語言維度 Six Language Dimensions

### 1. 流行語言 (Popular Languages)
**語言:** Python, JavaScript, TypeScript, Go, Rust  
**用途:** 快速原型、治理自動化、跨平台工具  
**示例:** `intelligent-automation/`, `scripts/`

### 2. 服務器端語言 (Server-side Languages)
**語言:** Java, C#, Node.js, Kotlin, Scala  
**用途:** 後端 API、微服務治理、企業系統  
**示例:** `core/`, `mcp-servers/`

### 3. Web語言 (Web Languages)
**語言:** JavaScript, TypeScript, HTML, CSS  
**用途:** UI 治理觀測、前端 SDK、治理可視化  
**示例:** `auto-fix-bot-dashboard.html`, `advanced-system-src/`

### 4. 移動語言 (Mobile Languages)
**語言:** Swift, Kotlin, Dart, React Native  
**用途:** 移動端治理 SDK、觀測模組、跨平台工具  
**示例:** (未來模組)

### 5. 數據表示語言 (Data Representation Languages)
**語言:** JSON, YAML, XML, Protocol Buffers  
**用途:** 治理邊界文件、責任矩陣、事件日誌、配置管理  
**示例:** `.governance/`, `.auto-fix-bot.yml`, `cloud-agent-delegation.yml`

### 6. 其它語言 (Other Languages)
**語言:** C++, Haskell, Elixir, Zig, C  
**用途:** 高性能治理模組、安全性強化、函數式治理邏輯  
**示例:** (未來模組)

---

## 🔧 使用指南 Usage Guide

### 查看模組需求 Check Module Requirements

```bash
# 查看完整映射
cat .governance/module-environment-matrix.yml

# 查看語言維度文檔
cat .governance/LANGUAGE_DIMENSION_MAPPING.md
```

### 條件式部署 Conditional Deployment

```bash
# 使用智能部署腳本
./scripts/conditional-deploy.sh

# 輸出示例：
# ✓ Python module detected: intelligent-automation
#   Installing from requirements.txt
# ✓ Node.js module detected: core
#   Installing npm dependencies
```

### 添加新模組 Add New Module

1. **在 `module-environment-matrix.yml` 中定義模組**
```yaml
modules:
  your-new-module:
    primary_language: "python"
    language_dimension: "popular_languages"
    runtime: "python >= 3.8"
    optional_dependencies:
      - "some-library: for specific feature"
    deployment_conditions:
      - "requires_python: true"
```

2. **更新條件式部署腳本**
```bash
# 在 conditional-deploy.sh 中添加檢測邏輯
if [ -d "$ROOT_DIR/your-new-module" ]; then
    install_python_deps "$ROOT_DIR/your-new-module"
fi
```

3. **創建模組的 README**
- 說明環境需求
- 標記可選依賴
- 提供安裝指引

### 驗證治理合規性 Validate Governance Compliance

檢查清單：

- [ ] 模組未硬編碼特定 Python 版本（如 3.10）
- [ ] 外部服務（如 ModelScope API）標記為可選
- [ ] 每個模組在 `module-environment-matrix.yml` 中有定義
- [ ] 部署腳本使用條件式邏輯
- [ ] 語言邊界在文檔中清晰說明
- [ ] 可選依賴在 README 中明確標註

---

## 📚 相關文檔 Related Documentation

### 治理文檔 Governance Documents
- [Module Environment Matrix](module-environment-matrix.yml) - 模組環境需求映射
- [Language Dimension Mapping](LANGUAGE_DIMENSION_MAPPING.md) - 語言維度映射

### 部署工具 Deployment Tools
- [Conditional Deploy Script](../scripts/conditional-deploy.sh) - 條件式部署腳本

### 模組文檔 Module Documentation
- [Intelligent Automation](../intelligent-automation/README.md) - Python 模組（可選依賴）
- [Core Services](../core/README.md) - Node.js 服務
- [MCP Servers](../mcp-servers/README.md) - TypeScript 服務

### 配置文檔 Configuration Documents
- [Auto-Fix Bot Config](../.auto-fix-bot.yml) - Bot 配置
- [Cloud Agent Delegation](../cloud-agent-delegation.yml) - 代理委派配置

---

## 🎓 最佳實踐 Best Practices

### 1. 分層治理 Layered Governance

```
治理層 (Governance Layer)
  ↓ 定義需求映射
配置層 (Configuration Layer)
  ↓ 實現條件式邏輯
部署層 (Deployment Layer)
  ↓ 執行智能安裝
代碼層 (Code Layer)
  ↓ 優雅降級
```

### 2. 依賴管理原則

- **必需依賴 (Required):** 模組核心功能所需
- **可選依賴 (Optional):** 增強功能但非必需
- **開發依賴 (Dev):** 僅開發和測試時需要

### 3. 版本策略

- 使用最小版本需求：`>= 3.8` ✅
- 避免固定版本：`== 3.10` ❌
- 說明版本選擇原因

### 4. 錯誤處理

當缺少依賴時：
- **必需依賴:** 提供清晰的錯誤訊息和安裝指引
- **可選依賴:** 優雅降級，記錄警告日誌
- **開發依賴:** 僅在開發模式下檢查

---

## 🔍 治理驗證 Governance Validation

### 自動化檢查 Automated Checks

```bash
# 檢查硬編碼依賴
grep -r "python==3.10" . --exclude-dir=node_modules

# 驗證模組定義
python -c "import yaml; yaml.safe_load(open('.governance/module-environment-matrix.yml'))"

# 測試條件式部署
./scripts/conditional-deploy.sh --dry-run
```

### 手動審查 Manual Review

定期審查：
1. 新增模組是否在治理文件中定義
2. 依賴是否正確分類（必需/可選/開發）
3. 部署腳本是否處理新模組類型
4. 文檔是否保持更新

---

## 💡 常見問題 FAQ

### Q1: 為什麼不能硬編碼 Python 3.10？

**A:** 硬編碼會強制所有項目使用相同版本，造成：
- 部署困難（某些環境可能不支援）
- 升級困難（需要同時升級所有項目）
- 治理失效（無法針對不同模組優化）

### Q2: 如何確定依賴是必需還是可選？

**A:** 問自己：
- 核心功能能否在沒有此依賴時運行？ → 可選
- 模組是否完全無法啟動？ → 必需
- 僅開發/測試時需要？ → 開發依賴

### Q3: 條件式部署如何與 CI/CD 集成？

**A:** 在 CI/CD 配置中：
```yaml
- name: Conditional Deployment
  run: ./scripts/conditional-deploy.sh
```

腳本會自動檢測模組類型並安裝對應依賴。

### Q4: 如何處理語言邊界？

**A:** 遵循治理原則：
- 內部代碼：繁體中文
- 公開 API：雙語（中文 + 英文）
- 在需要切換語言的地方明確標註

---

## 📈 治理指標 Governance Metrics

追蹤以下指標確保治理有效：

| 指標 | 目標 | 當前 |
|------|------|------|
| 硬編碼依賴數量 | 0 | 0 ✅ |
| 模組定義覆蓋率 | 100% | 100% ✅ |
| 條件式部署成功率 | > 95% | 100% ✅ |
| 文檔同步率 | 100% | 100% ✅ |
| 語言邊界一致性 | 100% | 100% ✅ |

---

## 🔄 更新歷史 Update History

- **2025-11-25:** 初始版本
  - 創建模組環境映射
  - 定義六大語言維度
  - 實現條件式部署
  - 移除硬編碼依賴

---

**維護者 Maintainer:** SynergyMesh Team  
**最後更新 Last Updated:** 2025-11-25  
**版本 Version:** 1.0
