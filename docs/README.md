# SynergyMesh Documentation Portal
# 文檔入口

> 這是 SynergyMesh 所有文檔的統一入口。人類請從這裡開始，機器請讀 [knowledge_index.yaml](./knowledge_index.yaml)。
> This is the unified entry point for all SynergyMesh documentation. Humans start here; machines read [knowledge_index.yaml](./knowledge_index.yaml).

## 🤖 For Agents & Automation 給智能體和自動化工具

**Machine-readable knowledge index / 機器可讀知識索引:**
- **[knowledge_index.yaml](./knowledge_index.yaml)** - Structured document catalog with metadata
- Validate with: `python tools/docs/validate_index.py`

---

## 📚 Documentation Index 文檔索引

### 🏗️ Architecture 架構

核心架構設計和系統邊界定義。

| Document | Description |
|----------|-------------|
| **[Architecture Layers](./architecture/layers.md)** ⭐ | Five-layer architecture view with dependency rules |
| **[Repository Map](./architecture/repo-map.md)** ⭐ | Semantic boundaries and decision guides |
| [System Architecture](./architecture/SYSTEM_ARCHITECTURE.md) | Four-layer microservices architecture |
| [Deployment & Infrastructure](./architecture/DEPLOYMENT_INFRASTRUCTURE.md) | Docker, Kubernetes, CI/CD setup |
| [Code Quality Checks](./architecture/CODE_QUALITY_CHECKS.md) | Quality tools configuration |
| [Security & Config Checks](./architecture/SECURITY_CONFIG_CHECKS.md) | Security scanning and validation |

### 🤖 Automation & Agents 自動化與代理

AI 系統、自動化流程和智能代理。

| Document | Description |
|----------|-------------|
| **[Intelligent Automation](../automation/intelligent/README.md)** | Multi-agent AI code analysis system |
| **[Agent Services](../agent/README.md)** | Long-lifecycle business agents |
| **[MCP Servers](../mcp-servers/README.md)** | LLM tool endpoints (MCP protocol) |
| [Autonomous System](../automation/autonomous/README.md) | Drone/self-driving framework |
| [Auto-Assignment System](./AUTO_ASSIGNMENT_SYSTEM.md) | Intelligent task assignment |
| [Advanced Escalation](./ADVANCED_ESCALATION_SYSTEM.md) | Multi-level escalation system |

### 🏛️ Core Platform 核心平台

平台核心服務和執行環境。

| Document | Description |
|----------|-------------|
| **[Core Services](../core/README.md)** | Platform core capabilities |
| **[Runtime Environment](../runtime/README.md)** | Runtime hosting execution |
| [Execution Engine](../core/execution_engine/README.md) | Execution logic abstraction |
| [Execution Architecture](../core/execution_architecture/README.md) | Execution topology design |
| [Contract Service](../core/contract_service/README.md) | Contract management microservice |
| [External Contracts](../contracts/README.md) | API specs and schemas |

### ⚖️ Governance & Security 治理與安全

政策、規則、安全和合規。

| Document | Description |
|----------|-------------|
| [Governance](../governance/README.md) | Policies, rules, SBOM |
| [Vulnerability Management](./VULNERABILITY_MANAGEMENT.md) | CVE detection and response |
| [Secret Scanning](./SECRET_SCANNING.md) | Secret detection |
| [Security Training](./SECURITY_TRAINING.md) | Security best practices |

### 🚀 Getting Started 快速入門

| Document | Description |
|----------|-------------|
| [Quick Start Guide](./QUICK_START.md) | Get up and running quickly |
| [Copilot Setup](./COPILOT_SETUP.md) | GitHub Copilot integration |
| [Integration Guide](./INTEGRATION_GUIDE.md) | External system integration |

### 🔄 CI/CD & Operations CI/CD 與運維

| Document | Description |
|----------|-------------|
| [Auto Review & Merge](./AUTO_REVIEW_MERGE.md) | Automated PR workflow |
| [Dynamic CI Assistant](./DYNAMIC_CI_ASSISTANT.md) | Interactive CI system |
| [Cloud Delegation](./CLOUD_DELEGATION.md) | Distributed task processing |

---

## 🎯 Quick Navigation 快速導航

### By Role 按角色

| Role | Start Here | Then Read |
|------|------------|-----------|
| **New Developer** | [Quick Start](./QUICK_START.md) | [Examples](./EXAMPLES.md) → [Copilot Setup](./COPILOT_SETUP.md) |
| **DevOps Engineer** | [Deployment](./architecture/DEPLOYMENT_INFRASTRUCTURE.md) | [CI/CD](./AUTO_REVIEW_MERGE.md) → [Monitoring](./architecture/CODE_QUALITY_CHECKS.md) |
| **System Architect** | [Architecture Layers](./architecture/layers.md) | [Repo Map](./architecture/repo-map.md) → [System Design](./architecture/SYSTEM_ARCHITECTURE.md) |
| **Agent Developer** | [Repo Map](./architecture/repo-map.md) | [Agent Services](../agent/README.md) → [MCP Servers](../mcp-servers/README.md) |
| **Security Engineer** | [Security Checks](./architecture/SECURITY_CONFIG_CHECKS.md) | [Vulnerability Mgmt](./VULNERABILITY_MANAGEMENT.md) → [Governance](../governance/README.md) |

### By Domain 按領域

| Domain | Key Documents |
|--------|---------------|
| **Architecture** | [layers.md](./architecture/layers.md), [repo-map.md](./architecture/repo-map.md) |
| **Autonomous Systems** | [autonomous/README.md](../automation/autonomous/README.md), [QUICKSTART.md](../automation/autonomous/docs-examples/QUICKSTART.md) |
| **AI/Agents** | [intelligent/README.md](../automation/intelligent/README.md), [agent/README.md](../agent/README.md) |
| **Security** | [SECURITY_CONFIG_CHECKS.md](./architecture/SECURITY_CONFIG_CHECKS.md), [governance/](../governance/) |
| **CI/CD** | [AUTO_REVIEW_MERGE.md](./AUTO_REVIEW_MERGE.md), [DYNAMIC_CI_ASSISTANT.md](./DYNAMIC_CI_ASSISTANT.md) |

---

## 📋 Document Structure 文檔結構

```
docs/
├── README.md                  # 📍 You are here (Documentation Portal)
├── knowledge_index.yaml       # 🤖 Machine-readable index
├── architecture/              # 🏗️ Architecture documentation
│   ├── layers.md             # Architecture layers view
│   ├── repo-map.md           # Semantic boundaries
│   ├── SYSTEM_ARCHITECTURE.md
│   └── configuration/        # Config files & scripts
├── ci-cd/                    # CI/CD documentation
├── operations/               # Operations guides
├── security/                 # Security documentation
└── *.md                      # Feature-specific docs

tools/docs/
└── validate_index.py         # 🔍 Index validator
```

---

## 🆕 Recent Updates 最近更新

- **2025-11-30**: Phase 2 documentation system upgrade
  - Added `knowledge_index.yaml` for machine-readable document catalog
  - Added `validate_index.py` for index validation
  - Updated documentation portal structure

- **2025-11-30**: Phase 1 architecture documentation
  - Added architecture layers (`layers.md`) and repository map (`repo-map.md`)
  - Added boundary READMEs to key directories
  - Renamed `core/contracts/` to `core/contract_service/`

- **2025-11-21**: Initial comprehensive architecture documentation
  - System architecture design
  - Deployment and infrastructure guides
  - Code quality checks implementation

---

## 🤝 Contributing to Documentation 貢獻文檔

1. Check existing documentation for gaps
2. Follow the established format and style
3. **Update [knowledge_index.yaml](./knowledge_index.yaml)** when adding new docs
4. Run `python tools/docs/validate_index.py` before submitting
5. Submit a Pull Request

## 🔗 Related Resources 相關資源

- [Main README](../README.md) - Project overview
- [Contributing Guide](../CONTRIBUTING.md) - How to contribute
- [Security Policy](../SECURITY.md) - Security practices

---

**Last Updated 最後更新**: 2025-11-30  
**Documentation Version 文檔版本**: 2.0.0  
**Maintained by 維護者**: SynergyMesh Development Team
