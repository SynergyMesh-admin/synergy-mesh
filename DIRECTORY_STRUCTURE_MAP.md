# SynergyMesh 倉庫完整目錄結構圖譜（含註解）
# Repository Complete Directory Structure Map (Annotated)

**Generated:** 2025-11-30 UTC  
**Repository:** Unmanned-Island-admin/SynergyMesh  
**Version:** 2.0 (Annotated Edition)

---

## 📋 說明 / Description

此文件包含完整的倉庫目錄結構，每個檔案和目錄後面都附有說明註解。

This file contains the complete repository directory structure with description annotations for each file and directory.

**圖例 / Legend:**
- 📁 目錄 / Directory
- 📄 文件 / File
- 🔧 配置 / Configuration
- 📜 腳本 / Script
- 🧪 測試 / Test
- 📖 文檔 / Documentation

---

## 🗂️ 完整目錄結構 / Complete Directory Structure


### 🔒 隱藏目錄 / Hidden Directories

```
.
├── .autofix/                                    # 🔧 自動修復配置目錄 / Auto-fix configuration directory
│   ├── rules/                                   # 📁 修復規則目錄 / Fix rules directory
│   │   ├── performance-rules.yaml               # ⚡ 效能優化規則 / Performance optimization rules
│   │   └── security-rules.yaml                  # 🔒 安全修復規則 / Security fix rules
│   └── config.json                              # ⚙️ 自動修復主配置 / Main auto-fix configuration
│
├── .ci/                                         # 🔄 CI 配置目錄 / CI configuration directory
│   └── policy-gate.yaml                         # 🚪 CI 策略閘門配置 / CI policy gate configuration
│
├── .config/                                     # ⚙️ 專案配置目錄 / Project configuration directory
│   └── conftest/                                # 🧪 Conftest 配置 / Conftest configuration
│       └── policies/                            # 📜 策略定義目錄 / Policy definitions directory
│           ├── matechat-integration/            # 🔗 MateChat 整合策略 / MateChat integration policy
│           │   ├── README.md                    # �� 整合說明文檔 / Integration documentation
│           │   └── integration-policy.rego      # 📜 整合策略規則 / Integration policy rules
│           └── naming_policy.rego               # 📛 命名規範策略 / Naming convention policy
│
├── .devcontainer/                               # 🐳 開發容器配置目錄 / Dev container configuration directory
│   ├── automation/                              # 🤖 容器自動化腳本 / Container automation scripts
│   │   ├── auto-pilot.js                        # ✈️ 自動導航腳本 / Auto-pilot script
│   │   ├── code-generator.ts                    # 💻 代碼生成器 / Code generator
│   │   ├── deployment-drone.sh                  # 🚁 部署無人機腳本 / Deployment drone script
│   │   └── drone-coordinator.py                 # 🎮 無人機協調器 / Drone coordinator
│   ├── environments/                            # 🌍 環境配置目錄 / Environment configs directory
│   │   ├── development.env                      # 🔧 開發環境變數 / Development environment variables
│   │   ├── production.env                       # 🚀 生產環境變數 / Production environment variables
│   │   └── staging.env                          # 🎭 預演環境變數 / Staging environment variables
│   ├── templates/                               # 📄 專案模板目錄 / Project templates directory
│   │   ├── connector-template/                  # 🔌 連接器模板 / Connector template
│   │   ├── integration-template/                # 🔗 整合模板 / Integration template
│   │   └── service-template/                    # 🔧 服務模板 / Service template
│   ├── CHANGELOG.md                             # 📝 變更日誌 / Change log
│   ├── Dockerfile                               # 🐳 開發容器映像配置 / Dev container image config
│   ├── KB.md                                    # 📚 知識庫文檔 / Knowledge base document
│   ├── QUICK_START.md                           # 🚀 快速入門指南 / Quick start guide
│   ├── README.md                                # 📖 開發容器說明 / Dev container documentation
│   ├── devcontainer.json                        # ⚙️ DevContainer 主配置 / DevContainer main config
│   ├── docker-compose.yml                       # 🐳 Docker Compose 配置 / Docker Compose config
│   ├── post-create.sh                           # 📜 容器建立後腳本 / Post-create script
│   ├── post-start.sh                            # 📜 容器啟動後腳本 / Post-start script
│   ├── requirements.txt                         # 📦 Python 依賴清單 / Python dependencies
│   └── setup.sh                                 # 🔧 環境設置腳本 / Environment setup script
│
├── .docker-templates/                           # 🐳 Docker 模板目錄 / Docker templates directory
│   ├── NODEJS_USER_SETUP.md                     # 📚 Node.js 用戶設置指南 / Node.js user setup guide
│   └── validate-dockerfiles.sh                  # ✅ Dockerfile 驗證腳本 / Dockerfile validation script
│
├── .github/                                     # 🐙 GitHub 配置目錄 / GitHub configuration directory
│   ├── ISSUE_TEMPLATE/                          # 📝 Issue 模板目錄 / Issue templates directory
│   │   ├── bug_report.yml                       # 🐛 錯誤報告模板 / Bug report template
│   │   ├── config.yml                           # ⚙️ Issue 模板配置 / Issue template config
│   │   ├── documentation.yml                    # 📖 文檔問題模板 / Documentation issue template
│   │   └── feature_request.yml                  # ✨ 功能請求模板 / Feature request template
│   ├── agents/                                  # 🤖 GitHub Copilot Agent 配置 / Copilot Agent configs
│   │   └── my-agent.agent.md                    # 🤖 自定義代理定義 / Custom agent definition
│   ├── codeql/                                  # 🔍 CodeQL 分析配置 / CodeQL analysis configuration
│   │   ├── custom-queries/                      # �� 自定義查詢目錄 / Custom queries directory
│   │   │   ├── enterprise-security.ql           # 🔒 企業安全查詢 / Enterprise security query
│   │   │   └── qlpack.yml                       # 📦 QL 包配置 / QL pack configuration
│   │   └── codeql-config.yml                    # ⚙️ CodeQL 主配置 / CodeQL main configuration
│   ├── profile/                                 # 👤 組織配置文件目錄 / Organization profile directory
│   │   └── README.md                            # 📖 組織說明 / Organization description
│   ├── scripts/                                 # 📜 GitHub Actions 腳本 / GitHub Actions scripts
│   │   ├── auto-fix-imports.sh                  # 🔧 自動修復導入腳本 / Auto-fix imports script
│   │   ├── risk_assessment.py                   # ⚠️ 風險評估腳本 / Risk assessment script
│   │   └── solution_generator.py                # 💡 解決方案生成器 / Solution generator
│   ├── secret-scanning/                         # 🔐 密鑰掃描配置目錄 / Secret scanning config directory
│   │   └── custom-patterns.yml                  # 🔍 自定義掃描模式 / Custom scanning patterns
│   ├── workflows/                               # ⚡ GitHub Actions 工作流程 / GitHub Actions workflows
│   │   ├── auto-review-merge.yml                # 🔄 自動審核合併流程 / Auto review merge workflow
│   │   ├── autofix-bot.yml                      # 🤖 自動修復機器人流程 / Autofix bot workflow
│   │   ├── codeql.yml                           # 🔍 CodeQL 分析流程 / CodeQL analysis workflow
│   │   ├── main-ci.yml                          # 🔄 主 CI 流程 / Main CI workflow
│   │   ├── release.yml                          # 🚀 發布流程 / Release workflow
│   │   ├── security-audit.yml                   # 🔒 安全審計流程 / Security audit workflow
│   │   ├── slsa-provenance.yml                  # 🔐 SLSA 溯源流程 / SLSA provenance workflow
│   │   └── [... 更多工作流 / more workflows]    # ⚡ 其他工作流程 / Other workflows
│   ├── CODEOWNERS                               # 👥 代碼負責人定義 / Code owners definition
│   ├── FUNDING.yml                              # 💰 贊助配置 / Funding configuration
│   ├── PULL_REQUEST_TEMPLATE.md                 # 📝 PR 模板 / Pull request template
│   ├── copilot-instructions.md                  # 🤖 Copilot 自定義指令 / Copilot custom instructions
│   ├── dependabot.yml                           # 🔄 Dependabot 依賴更新配置 / Dependabot configuration
│   └── security-policy.yml                      # 🔒 安全策略配置 / Security policy configuration
│
├── .github-private/                             # 🔒 私有 GitHub 配置 / Private GitHub configuration
│   ├── agents/                                  # 🤖 私有代理配置 / Private agent configs
│   ├── config/                                  # ⚙️ 私有配置文件 / Private configuration files
│   ├── templates/                               # 📄 私有模板 / Private templates
│   └── README.md                                # 📖 私有配置說明 / Private config documentation
│
├── .governance/                                 # ⚖️ 治理配置目錄 / Governance configuration directory
│   ├── deployment/                              # 🚀 部署治理策略 / Deployment governance policies
│   ├── LANGUAGE_DIMENSION_MAPPING.md            # 🌐 語言維度映射 / Language dimension mapping
│   ├── README.md                                # 📖 治理說明文檔 / Governance documentation
│   ├── module-environment-matrix.yml            # 📊 模組環境矩陣 / Module environment matrix
│   ├── policies.yaml                            # 📜 主治理策略 / Main governance policies
│   └── registry.yaml                            # 📋 治理註冊表 / Governance registry
│
├── .registry/                                   # 📋 模組註冊目錄 / Module registry directory
│   ├── module-A.yaml                            # 📦 模組 A 註冊 / Module A registry
│   ├── module-contracts-l1.yaml                 # 📝 L1 合約模組註冊 / L1 contract module registry
│   └── schema.json                              # 📐 註冊表 Schema 定義 / Registry schema definition
│
├── .vscode/                                     # 💻 VS Code 配置目錄 / VS Code configuration directory
│   ├── extensions.json                          # 🧩 推薦擴展清單 / Recommended extensions list
│   ├── mcp.json                                 # 🔌 MCP 編輯器配置 / MCP editor configuration
│   ├── settings.json                            # ⚙️ 編輯器設置 / Editor settings
│   └── tasks.json                               # 📋 任務定義 / Task definitions
```


### 📁 .git 目錄 / .git Directory

```
├── .git/                                        # 📁 Git 版本控制目錄 / Git version control directory
│   ├── hooks/                                   # 🪝 Git 鉤子腳本目錄 / Git hook scripts directory
│   │   ├── applypatch-msg.sample                # 📜 應用補丁訊息範例 / Apply patch message sample
│   │   ├── commit-msg.sample                    # 📜 提交訊息範例 / Commit message sample
│   │   ├── fsmonitor-watchman.sample            # 📜 文件監控範例 / File monitor sample
│   │   ├── post-update.sample                   # 📜 更新後鉤子範例 / Post-update sample
│   │   ├── pre-applypatch.sample                # 📜 應用補丁前範例 / Pre-applypatch sample
│   │   ├── pre-commit.sample                    # 📜 提交前鉤子範例 / Pre-commit sample
│   │   ├── pre-merge-commit.sample              # 📜 合併提交前範例 / Pre-merge-commit sample
│   │   ├── pre-push.sample                      # 📜 推送前鉤子範例 / Pre-push sample
│   │   ├── pre-rebase.sample                    # 📜 重設基底前範例 / Pre-rebase sample
│   │   ├── pre-receive.sample                   # 📜 接收前鉤子範例 / Pre-receive sample
│   │   ├── prepare-commit-msg.sample            # 📜 準備提交訊息範例 / Prepare-commit-msg sample
│   │   ├── push-to-checkout.sample              # 📜 推送到檢出範例 / Push-to-checkout sample
│   │   ├── sendemail-validate.sample            # 📜 發送郵件驗證範例 / Sendemail-validate sample
│   │   └── update.sample                        # 📜 更新鉤子範例 / Update sample
│   ├── info/                                    # ℹ️ Git 資訊目錄 / Git info directory
│   │   └── exclude                              # 🚫 本地排除規則 / Local exclude rules
│   ├── logs/                                    # 📜 Git 日誌目錄 / Git logs directory
│   │   ├── HEAD                                 # 📍 HEAD 日誌 / HEAD log
│   │   └── refs/                                # 🔖 引用日誌目錄 / Reference logs directory
│   │       ├── heads/                           # 🌿 分支日誌 / Branch logs
│   │       └── remotes/                         # 🌐 遠端日誌 / Remote logs
│   ├── objects/                                 # 📦 Git 物件資料庫 / Git object database
│   │   ├── info/                                # ℹ️ 物件資訊 / Object info
│   │   └── pack/                                # 📦 打包物件 / Packed objects
│   ├── refs/                                    # 🔖 Git 引用目錄 / Git references directory
│   │   ├── heads/                               # 🌿 分支引用 / Branch references
│   │   ├── remotes/                             # 🌐 遠端引用 / Remote references
│   │   │   └── origin/                          # 🌐 Origin 遠端 / Origin remote
│   │   └── tags/                                # 🏷️ 標籤引用 / Tag references
│   ├── COMMIT_EDITMSG                           # 📝 最後提交訊息 / Last commit message
│   ├── FETCH_HEAD                               # 🔄 最後獲取頭 / Last fetch head
│   ├── HEAD                                     # 📍 當前分支指標 / Current branch pointer
│   ├── ORIG_HEAD                                # 📍 原始 HEAD / Original HEAD
│   ├── config                                   # ⚙️ 本地 Git 配置 / Local Git configuration
│   ├── description                              # 📝 倉庫描述 / Repository description
│   ├── index                                    # 📋 Git 索引（暫存區）/ Git index (staging area)
│   └── packed-refs                              # 📦 打包引用 / Packed references
```


### 📦 node_modules 目錄 / node_modules Directory

```
├── node_modules/                                # 📦 NPM 依賴套件目錄 / NPM dependency packages
│   │                                            # ⚠️ 此目錄包含約 30,000+ 文件 / Contains ~30,000+ files
│   │                                            # ⚠️ 以下為主要套件摘要 / Below is a summary of major packages
│   │
│   ├── @babel/                                  # 🔄 Babel 轉譯器套件集 / Babel transpiler packages
│   │   ├── code-frame/                          # 🖼️ 代碼框架生成 / Code frame generation
│   │   ├── core/                                # ⚙️ Babel 核心 / Babel core
│   │   ├── generator/                           # 📝 代碼生成器 / Code generator
│   │   ├── parser/                              # 📖 JavaScript 解析器 / JavaScript parser
│   │   ├── traverse/                            # 🔍 AST 遍歷器 / AST traverser
│   │   └── types/                               # 📘 AST 類型定義 / AST type definitions
│   │
│   ├── @eslint/                                 # 📏 ESLint 核心套件集 / ESLint core packages
│   │   ├── config-array/                        # ⚙️ 配置陣列處理 / Config array handling
│   │   ├── eslintrc/                            # 📄 ESLint RC 配置 / ESLint RC configuration
│   │   ├── js/                                  # 📜 JavaScript 規則 / JavaScript rules
│   │   └── object-schema/                       # 📐 物件 Schema 驗證 / Object schema validation
│   │
│   ├── @sigstore/                               # 🔐 Sigstore 簽名套件集 / Sigstore signing packages
│   │   ├── bundle/                              # 📦 簽名包處理 / Signature bundle handling
│   │   ├── core/                                # ⚙️ Sigstore 核心 / Sigstore core
│   │   ├── sign/                                # ✍️ 簽名功能 / Signing functionality
│   │   ├── tuf/                                 # 🔒 TUF 更新框架 / TUF update framework
│   │   └── verify/                              # ✅ 簽名驗證 / Signature verification
│   │
│   ├── @types/                                  # 📘 TypeScript 類型定義集 / TypeScript type definitions
│   │   ├── express/                             # 🚀 Express 類型 / Express types
│   │   ├── jest/                                # 🧪 Jest 類型 / Jest types
│   │   ├── node/                                # 📦 Node.js 類型 / Node.js types
│   │   └── react/                               # ⚛️ React 類型 / React types
│   │
│   ├── @typescript-eslint/                      # 📘 TypeScript ESLint 套件 / TypeScript ESLint packages
│   │   ├── eslint-plugin/                       # 🔌 ESLint 插件 / ESLint plugin
│   │   ├── parser/                              # 📖 TypeScript 解析器 / TypeScript parser
│   │   └── typescript-estree/                   # 🌳 TypeScript ESTree / TypeScript ESTree
│   │
│   ├── express/                                 # 🚀 Express Web 框架 / Express web framework
│   │   ├── lib/                                 # 📚 Express 庫文件 / Express library files
│   │   │   ├── application.js                   # 📱 應用程式邏輯 / Application logic
│   │   │   ├── request.js                       # 📥 請求處理 / Request handling
│   │   │   ├── response.js                      # 📤 響應處理 / Response handling
│   │   │   └── router/                          # 🛤️ 路由器 / Router
│   │   └── index.js                             # 🚀 入口點 / Entry point
│   │
│   ├── jest/                                    # 🧪 Jest 測試框架 / Jest testing framework
│   │   ├── bin/                                 # 📦 可執行文件 / Executables
│   │   └── index.js                             # 🚀 入口點 / Entry point
│   │
│   ├── react/                                   # ⚛️ React UI 框架 / React UI framework
│   │   ├── cjs/                                 # 📦 CommonJS 版本 / CommonJS build
│   │   ├── umd/                                 # 📦 UMD 版本 / UMD build
│   │   └── index.js                             # 🚀 入口點 / Entry point
│   │
│   ├── typescript/                              # 📘 TypeScript 編譯器 / TypeScript compiler
│   │   ├── bin/                                 # 📦 tsc 可執行文件 / tsc executables
│   │   ├── lib/                                 # 📚 TypeScript 庫 / TypeScript library
│   │   └── package.json                         # 📦 套件配置 / Package configuration
│   │
│   ├── zod/                                     # ✅ Zod Schema 驗證庫 / Zod schema validation library
│   │   ├── lib/                                 # 📚 Zod 庫文件 / Zod library files
│   │   └── index.js                             # 🚀 入口點 / Entry point
│   │
│   └── [... 其他 600+ 套件 ...]                 # 📦 其他依賴套件 / Other dependencies
│       │                                        # 包括 / Including:
│       ├── axios/                               # 🌐 HTTP 客戶端 / HTTP client
│       ├── cors/                                # 🔓 CORS 中間件 / CORS middleware
│       ├── dotenv/                              # 🔐 環境變數載入 / Environment variable loading
│       ├── helmet/                              # 🛡️ 安全中間件 / Security middleware
│       ├── lodash/                              # 🔧 工具函數庫 / Utility functions library
│       ├── prettier/                            # ✨ 代碼格式化 / Code formatting
│       ├── webpack/                             # 📦 模組打包器 / Module bundler
│       └── [... 更多 / more ...]                # 📦 其他套件 / Other packages
```


### 📁 主要目錄 / Main Directories

```
├── agent/                                       # 🤖 代理程式目錄 / Agent programs directory
│   ├── auto-repair/                             # 🔧 自動修復代理 / Auto-repair agent
│   ├── code-analyzer/                           # 🔍 代碼分析代理 / Code analyzer agent
│   ├── dependency-manager/                      # 📦 依賴管理代理 / Dependency manager agent
│   ├── orchestrator/                            # 🎭 編排代理 / Orchestrator agent
│   ├── vulnerability-detector/                  # 🛡️ 漏洞偵測代理 / Vulnerability detector agent
│   └── runbook-executor.sh                      # 📋 Runbook 執行腳本 / Runbook executor script
│
├── attest-build-provenance-main/                # 🔐 建置認證溯源模組 / Build attestation provenance module
│   ├── .github/workflows/                       # ⚡ 認證模組工作流程 / Attestation module workflows
│   ├── __tests__/                               # 🧪 認證模組測試 / Attestation module tests
│   ├── predicate/                               # �� 認證謂詞定義 / Attestation predicate definitions
│   ├── src/                                     # 💻 認證模組源碼 / Attestation module source code
│   ├── action.yml                               # ⚡ GitHub Action 定義 / GitHub Action definition
│   ├── package.json                             # 📦 套件配置 / Package configuration
│   └── tsconfig.json                            # 📘 TypeScript 配置 / TypeScript configuration
│
├── automation/                                  # 🤖 自動化系統目錄 / Automation systems directory
│   ├── architect/                               # 🏗️ 自動化架構師 / Automation architect
│   │   └── [分析和修復引擎]                     # ⚙️ Analysis and repair engines
│   ├── autonomous/                              # 🚗 自主系統框架 / Autonomous systems framework
│   │   └── [五骨架自駕/無人機框架]              # 🚁 Five-skeleton drone/self-driving framework
│   ├── hyperautomation/                         # ⚡ 超自動化模組 / Hyperautomation module
│   │   └── [超自動化策略和治理]                 # 📜 Hyperautomation strategies and governance
│   ├── intelligent/                             # 🧠 智能自動化 / Intelligent automation
│   │   └── [多代理 AI 代碼分析系統]             # 🤖 Multi-agent AI code analysis system
│   └── zero_touch_deployment.py                 # 🚀 零接觸部署腳本 / Zero-touch deployment script
│
├── bridges/                                     # 🌉 系統橋接目錄 / System bridges directory
│   └── language_bridges.py                      # 🔗 語言橋接模組 / Language bridges module
│
├── config/                                      # ⚙️ 配置文件目錄 / Configuration files directory
│   ├── integrations/                            # 🔗 整合配置 / Integration configurations
│   │   ├── matechat/config.yaml                 # 💬 MateChat 配置 / MateChat configuration
│   │   ├── jira-integration.py                  # 🎫 Jira 整合 / Jira integration
│   │   └── slack-webhook.sh                     # 💬 Slack Webhook / Slack webhook
│   ├── ai-constitution.yaml                     # 📜 AI 治理憲章 / AI governance constitution
│   ├── auto-fix-bot.yml                         # 🤖 自動修復機器人配置 / Auto-fix bot configuration
│   ├── cloud-agent-delegation.yml               # ☁️ 雲代理委派配置 / Cloud agent delegation config
│   ├── drone-config.yml                         # 🚁 無人機配置 / Drone configuration
│   ├── monitoring.yaml                          # 📊 監控配置 / Monitoring configuration
│   ├── safety-mechanisms.yaml                   # 🛡️ 安全機制配置 / Safety mechanisms config
│   ├── system-manifest.yaml                     # 📋 系統宣告清單 / System manifest
│   ├── system-module-map.yaml                   # 🗺️ 系統模組映射 / System module map
│   └── unified-config-index.yaml                # 📇 統一配置索引 / Unified config index
│
├── contracts/                                   # 📝 外部合約定義目錄 / External contract definitions
│   └── external-api.json                        # 🌐 外部 API 合約 / External API contract
│
├── core/                                        # 🏛️ 核心平台服務目錄 / Core platform services directory
│   ├── advisory-database/                       # 📚 安全諮詢資料庫 / Security advisory database
│   ├── ai_constitution/                         # 📜 AI 治理憲章模組 / AI governance constitution module
│   ├── ci_error_handler/                        # 🔧 CI 錯誤處理器 / CI error handler
│   ├── cloud_agent_delegation/                  # ☁️ 雲代理委派模組 / Cloud agent delegation module
│   ├── contracts/contracts-L1/                  # 📝 L1 層合約服務 / Layer 1 contract services
│   │   ├── ai-chat-service/                     # 💬 AI 聊天服務 / AI chat service
│   │   └── contracts/                           # 📝 合約核心服務 / Contract core services
│   │       ├── src/                             # 💻 源碼 / Source code
│   │       │   ├── controllers/                 # 🎮 控制器 / Controllers
│   │       │   ├── middleware/                  # 🔌 中間件 / Middleware
│   │       │   ├── services/                    # 🔧 服務層 / Service layer
│   │       │   └── types/                       # 📘 類型定義 / Type definitions
│   │       ├── deploy/                          # 🚀 部署配置 / Deployment configs
│   │       └── web/                             # 🌐 Web 前端 / Web frontend
│   ├── execution_architecture/                  # 🏗️ 執行架構 / Execution architecture
│   ├── execution_engine/                        # ⚙️ 執行引擎 / Execution engine
│   ├── main_system/                             # 🎛️ 主系統核心 / Main system core
│   ├── mcp_servers_enhanced/                    # 🖥️ 增強型 MCP 伺服器 / Enhanced MCP servers
│   ├── monitoring_system/                       # 📊 監控系統 / Monitoring system
│   ├── safety_mechanisms/                       # 🛡️ 安全機制 / Safety mechanisms
│   ├── slsa_provenance/                         # 🔐 SLSA 溯源認證 / SLSA provenance attestation
│   ├── tech_stack/                              # 🔧 技術棧定義 / Tech stack definitions
│   ├── training_system/                         # 🎓 訓練系統 / Training system
│   ├── unified_integration/                     # 🔗 統一整合層 / Unified integration layer
│   ├── virtual_experts/                         # 👨‍💼 虛擬專家系統 / Virtual experts system
│   ├── yaml_module_system/                      # 📄 YAML 模組系統 / YAML module system
│   ├── ai_decision_engine.py                    # 🧠 AI 決策引擎 / AI decision engine
│   ├── auto_bug_detector.py                     # 🐛 自動缺陷偵測 / Auto bug detector
│   ├── auto_governance_hub.py                   # ⚖️ 自動治理中心 / Auto governance hub
│   ├── autonomous_trust_engine.py               # 🤝 自主信任引擎 / Autonomous trust engine
│   ├── context_understanding_engine.py          # 🔍 上下文理解引擎 / Context understanding engine
│   └── hallucination_detector.py                # 🎭 幻覺偵測器 / Hallucination detector
│
├── docs/                                        # 📚 文件目錄 / Documentation directory
│   ├── architecture/                            # 🏗️ 架構文件 / Architecture documentation
│   │   ├── configuration/                       # ⚙️ 配置文件 / Configuration docs
│   │   ├── DIRECTORY_STRUCTURE.md               # 📁 目錄結構說明 / Directory structure docs
│   │   └── SYSTEM_ARCHITECTURE.md               # 🏛️ 系統架構說明 / System architecture docs
│   ├── automation/                              # 🤖 自動化文件 / Automation documentation
│   ├── ci-cd/                                   # 🔄 CI/CD 文件 / CI/CD documentation
│   ├── operations/                              # 🔧 運維文件 / Operations documentation
│   ├── reports/                                 # 📊 報告文件 / Report documentation
│   ├── security/                                # 🔒 安全文件 / Security documentation
│   └── [... 其他文檔 / other docs]              # 📖 其他說明文檔 / Other documentation
│
├── frontend/                                    # 🎨 前端應用目錄 / Frontend applications directory
│   └── ui/                                      # 💻 系統 UI 源碼 / System UI source code
│       ├── core/analyzers/                      # 🔍 核心分析器 / Core analyzers
│       ├── deploy/                              # 🚀 部署配置 / Deployment configs
│       ├── k8s/                                 # ☸️ Kubernetes 配置 / Kubernetes configs
│       ├── scripts/                             # 📜 建置腳本 / Build scripts
│       ├── services/                            # 🔌 服務層 / Service layer
│       └── src/                                 # 💻 源碼 / Source code
│           ├── components/                      # 🧩 React 組件 / React components
│           └── lib/                             # 📚 工具庫 / Utility library
│
├── governance/                                  # ⚖️ 治理與策略目錄 / Governance and policies directory
│   ├── audit/                                   # 📋 稽核配置 / Audit configuration
│   ├── policies/                                # 📜 策略定義 / Policy definitions
│   ├── rules/                                   # 📏 治理規則 / Governance rules
│   ├── sbom/                                    # 📦 軟體物料清單 / Software Bill of Materials
│   └── schemas/                                 # 📐 Schema 定義 / Schema definitions
│
├── infrastructure/                              # 🏗️ 基礎設施目錄 / Infrastructure directory
│   ├── canary/                                  # 🐦 金絲雀部署配置 / Canary deployment configs
│   ├── drift/                                   # 📈 漂移檢測配置 / Drift detection configs
│   ├── kubernetes/                              # ☸️ Kubernetes 配置 / Kubernetes configurations
│   │   ├── phase2/                              # ☸️ Phase 2 K8s 部署 / Phase 2 K8s deployments
│   │   │   ├── 01-namespace-rbac/               # 🔐 命名空間和 RBAC / Namespace and RBAC
│   │   │   ├── 02-storage/                      # 💾 存儲配置 / Storage configs
│   │   │   ├── 03-secrets-config/               # 🔒 密鑰配置 / Secrets configs
│   │   │   ├── 04-databases/                    # 🗄️ 資料庫配置 / Database configs
│   │   │   ├── 05-core-services/                # 🏛️ 核心服務 / Core services
│   │   │   ├── 06-monitoring/                   # 📊 監控服務 / Monitoring services
│   │   │   ├── 07-logging/                      # 📝 日誌服務 / Logging services
│   │   │   ├── 08-ingress-gateway/              # 🚪 入口閘道 / Ingress gateway
│   │   │   ├── 09-backup-recovery/              # 💾 備份恢復 / Backup recovery
│   │   │   ├── 10-testing/                      # 🧪 測試配置 / Testing configs
│   │   │   ├── 11-ci-cd/                        # 🔄 CI/CD 配置 / CI/CD configs
│   │   │   └── 12-security/                     # 🔒 安全配置 / Security configs
│   │   └── [... 其他 K8s 配置 / other configs]  # ☸️ 其他 Kubernetes 配置
│   └── monitoring/                              # 📊 監控配置 / Monitoring configurations
│
├── mcp-servers/                                 # 🖥️ MCP 伺服器實作目錄 / MCP server implementations
│   ├── deploy/                                  # 🚀 部署配置 / Deployment configs
│   ├── code-analyzer.js                         # 🔍 代碼分析伺服器 / Code analyzer server
│   ├── security-scanner.js                      # 🔒 安全掃描伺服器 / Security scanner server
│   ├── slsa-validator.js                        # ✅ SLSA 驗證伺服器 / SLSA validator server
│   ├── test-generator.js                        # 🧪 測試生成伺服器 / Test generator server
│   ├── doc-generator.js                         # 📄 文件生成伺服器 / Doc generator server
│   └── package.json                             # 📦 套件配置 / Package configuration
│
├── ops/                                         # 🔧 運維目錄 / Operations directory
│   ├── artifacts/reports/schema/                # 📐 報告 Schema / Report schemas
│   ├── migration/                               # 🔄 遷移工具 / Migration tools
│   │   ├── scripts/                             # 📜 遷移腳本 / Migration scripts
│   │   └── templates/                           # 📄 遷移模板 / Migration templates
│   ├── onboarding/                              # 🎓 入門指南 / Onboarding guides
│   ├── reports/                                 # 📊 運維報告 / Operations reports
│   └── runbooks/                                # 📋 運維手冊 / Runbooks
│
├── runtime/                                     # ⚡ 運行時目錄 / Runtime directory
│   └── mind_matrix/                             # 🧠 Mind Matrix 運行時 / Mind Matrix runtime
│       ├── __init__.py                          # 📦 模組初始化 / Module initialization
│       ├── executive_auto.py                    # 🤖 執行自動化 / Executive automation
│       └── main.py                              # 🚀 主入口 / Main entry
│
├── shared/                                      # 📦 共用資源目錄 / Shared resources directory
│   ├── config/                                  # ⚙️ 共用配置 / Shared configurations
│   ├── constants/                               # 📝 共用常數 / Shared constants
│   ├── utils/                                   # 🔧 共用工具 / Shared utilities
│   └── README.md                                # 📖 共用資源說明 / Shared resources docs
│
├── tests/                                       # �� 測試目錄 / Tests directory
│   ├── performance/                             # ⚡ 效能測試 / Performance tests
│   │   ├── benchmark.js                         # 📊 基準測試 / Benchmark tests
│   │   └── load-test.js                         # 📈 負載測試 / Load tests
│   ├── unit/                                    # 🔬 單元測試 / Unit tests
│   │   ├── phases/                              # 📋 階段測試 / Phase tests
│   │   └── [... 測試文件 / test files]          # 🧪 測試文件 / Test files
│   └── vectors/                                 # 📊 測試向量 / Test vectors
│       ├── auto-fix-bot/                        # 🤖 自動修復測試向量 / Auto-fix test vectors
│       ├── cloud-agent-delegation/              # ☁️ 雲代理測試向量 / Cloud agent test vectors
│       └── osv-advisory/                        # 🔒 OSV 諮詢測試向量 / OSV advisory test vectors
│
├── tools/                                       # 🔧 工具目錄 / Tools directory
│   ├── ci/                                      # 🔄 CI 輔助工具 / CI helper tools
│   │   ├── contract-checker.js                  # 📝 合約檢查器 / Contract checker
│   │   └── language-checker.js                  # 🌐 語言檢查器 / Language checker
│   ├── scripts/                                 # 📜 自動化腳本 / Automation scripts
│   │   ├── artifacts/                           # 📦 產物腳本 / Artifact scripts
│   │   ├── backup/                              # 💾 備份腳本 / Backup scripts
│   │   ├── naming/                              # 📛 命名工具 / Naming tools
│   │   └── [... 其他腳本 / other scripts]       # 📜 其他腳本 / Other scripts
│   └── utilities/                               # 🛠️ 通用工具 / General utilities
│
├── v1-python-drones/                            # 🚁 V1 Python 無人機系統 / V1 Python drones system
│   ├── config/                                  # ⚙️ 無人機配置 / Drone configurations
│   ├── drones/                                  # 🚁 無人機實作 / Drone implementations
│   │   ├── autopilot_drone.py                   # ✈️ 自動駕駛無人機 / Autopilot drone
│   │   ├── base_drone.py                        # 🚁 基礎無人機類 / Base drone class
│   │   ├── coordinator_drone.py                 # 🎯 協調無人機 / Coordinator drone
│   │   └── deployment_drone.py                  # 🚀 部署無人機 / Deployment drone
│   ├── utils/                                   # 🔧 無人機工具 / Drone utilities
│   ├── main.py                                  # 🚀 主入口 / Main entry
│   └── README.md                                # 📖 說明文檔 / Documentation
│
├── v2-multi-islands/                            # 🏝️ V2 多島嶼系統 / V2 multi-islands system
│   ├── bridges/                                 # 🌉 島嶼橋接 / Island bridges
│   │   └── language_bridge.py                   # 🔗 語言橋接 / Language bridge
│   ├── config/                                  # ⚙️ 島嶼配置 / Island configurations
│   ├── islands/                                 # 🏝️ 島嶼實作 / Island implementations
│   │   ├── base_island.py                       # 🏝️ 基礎島嶼類 / Base island class
│   │   ├── go_island.py                         # 🐹 Go 島嶼 / Go island
│   │   ├── java_island.py                       # ☕ Java 島嶼 / Java island
│   │   ├── python_island.py                     # 🐍 Python 島嶼 / Python island
│   │   ├── rust_island.py                       # 🦀 Rust 島嶼 / Rust island
│   │   └── typescript_island.py                 # 📘 TypeScript 島嶼 / TypeScript island
│   ├── orchestrator/                            # 🎭 島嶼編排器 / Island orchestrator
│   ├── utils/                                   # 🔧 島嶼工具 / Island utilities
│   ├── main.py                                  # 🚀 主入口 / Main entry
│   └── README.md                                # 📖 說明文檔 / Documentation
```


### 📄 根目錄文件 / Root Directory Files

```
├── .auto-fix-bot.yml                            # 🤖 自動修復機器人配置 / Auto-fix bot configuration
├── .env.example                                 # 🔐 環境變數範例 / Environment variables example
├── .eslintrc.yaml                               # 📏 ESLint 配置 / ESLint configuration
├── .gitignore                                   # 🚫 Git 忽略規則 / Git ignore rules
├── .prettierrc                                  # ✨ Prettier 格式化配置 / Prettier formatting config
├── CHANGELOG.md                                 # 📝 變更日誌 / Change log
├── CODE_OF_CONDUCT.md                           # 📜 行為準則 / Code of conduct
├── CONTRIBUTING.md                              # 🤝 貢獻指南 / Contribution guide
├── Dockerfile                                   # 🐳 主 Docker 映像配置 / Main Docker image config
├── README.md                                    # 📖 專案主說明文件 (中文) / Main README (Chinese)
├── README.en.md                                 # 📖 專案主說明文件 (英文) / Main README (English)
├── SECURITY.md                                  # 🔒 安全政策 / Security policy
├── auto-fix-bot-dashboard.html                  # 📊 自動修復機器人儀表板 / Auto-fix bot dashboard
├── automation-entry.sh                          # 🤖 自動化入口腳本 / Automation entry script
├── deploy.sh                                    # 🚀 部署腳本 / Deployment script
├── docker-compose.dev.yml                       # 🐳 Docker Compose 開發配置 / Docker Compose dev config
├── docker-compose.yml                           # 🐳 Docker Compose 生產配置 / Docker Compose prod config
├── jest.config.js                               # 🧪 Jest 測試框架配置 / Jest test framework config
├── nginx.conf                                   # 🌐 Nginx 配置 / Nginx configuration
├── package-lock.json                            # 🔒 NPM 依賴鎖定文件 / NPM dependency lock file
├── package.json                                 # 📦 Node.js 專案配置 / Node.js project configuration
├── pyproject.toml                               # 🐍 Python 專案配置 / Python project configuration
├── run-v2.sh                                    # ▶️ V2 系統啟動腳本 / V2 system startup script
└── tsconfig.json                                # 📘 TypeScript 配置 / TypeScript configuration
```

---

## 📊 統計摘要 / Statistics Summary

| 項目 / Item | 數量 / Count |
|-------------|-------------|
| 總目錄數 / Total Directories | ~3,546 |
| 總文件數 / Total Files | ~32,249 |
| 隱藏目錄 / Hidden Directories | 12 |
| 主要目錄 / Main Directories | 21 |
| node_modules 套件 / node_modules packages | ~600+ |

---

**Generated by:** SynergyMesh Directory Structure Generator  
**Last Updated:** 2025-11-30  
**Repository:** [Unmanned-Island-admin/SynergyMesh](https://github.com/Unmanned-Island-admin/SynergyMesh)
