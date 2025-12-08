# ═══════════════════════════════════════════════════════════════════════════════
#                    Unmanned Island System - Makefile
#                    MN-DOC & Knowledge Graph Generation Automation
# ═══════════════════════════════════════════════════════════════════════════════
#
# Usage:
#   make mndoc           - Generate MN-DOC from README.md
#   make kg              - Build Knowledge Graph from repository
#   make superroot       - Project entities to SuperRoot format
#   make all-kg          - Run all generation tasks
#   make check-drift     - Check if generated files are up-to-date
#   make clean-generated - Remove all generated YAML files
#   make analyze-reports - Analyze root-level reports
#
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: mndoc kg superroot all-kg check-drift clean-generated analyze-reports help

# Default target
.DEFAULT_GOAL := help

# Python interpreter
PYTHON := python3

# Source files (source of truth)
README := README.md
MNDOC_OUTPUT := docs/generated-mndoc.yaml
KG_OUTPUT := docs/knowledge-graph.yaml
SUPERROOT_OUTPUT := docs/superroot-entities.yaml
REPORTS_ANALYSIS_MD := docs/reports-analysis.md
REPORTS_ANALYSIS_JSON := docs/reports-analysis.json

# ─────────────────────────────────────────────────────────────────────────────
# MN-DOC Generation
# ─────────────────────────────────────────────────────────────────────────────
mndoc:
	@echo "🔄 Generating MN-DOC from README.md..."
	$(PYTHON) tools/docs/generate_mndoc_from_readme.py \
		--readme $(README) \
		--output $(MNDOC_OUTPUT) \
		--verbose
	@echo "✅ MN-DOC generated: $(MNDOC_OUTPUT)"

# ─────────────────────────────────────────────────────────────────────────────
# Knowledge Graph Generation
# ─────────────────────────────────────────────────────────────────────────────
kg: mndoc
	@echo "🔄 Building Knowledge Graph..."
	$(PYTHON) tools/docs/generate_knowledge_graph.py \
		--repo-root . \
		--output $(KG_OUTPUT) \
		--verbose
	@echo "✅ Knowledge Graph generated: $(KG_OUTPUT)"

# ─────────────────────────────────────────────────────────────────────────────
# SuperRoot Entity Projection
# ─────────────────────────────────────────────────────────────────────────────
superroot: kg
	@echo "🔄 Projecting to SuperRoot entities..."
	@if [ -f "tools/docs/project_to_superroot.py" ]; then \
		$(PYTHON) tools/docs/project_to_superroot.py \
			--kg $(KG_OUTPUT) \
			--output $(SUPERROOT_OUTPUT) \
			--verbose; \
		echo "✅ SuperRoot entities generated: $(SUPERROOT_OUTPUT)"; \
	else \
		echo "⚠️  SuperRoot projection tool not found (optional)"; \
	fi

# ─────────────────────────────────────────────────────────────────────────────
# All Knowledge Graph Tasks
# ─────────────────────────────────────────────────────────────────────────────
all-kg: mndoc kg superroot
	@echo ""
	@echo "════════════════════════════════════════════════════════════════"
	@echo "  ✅ All MN-DOC & Knowledge Graph artifacts generated!"
	@echo "════════════════════════════════════════════════════════════════"
	@echo ""
	@echo "Generated files:"
	@echo "  - $(MNDOC_OUTPUT)"
	@echo "  - $(KG_OUTPUT)"
	@if [ -f "$(SUPERROOT_OUTPUT)" ]; then echo "  - $(SUPERROOT_OUTPUT)"; fi
	@echo ""
	@echo "Next steps:"
	@echo "  1. Review generated files: git diff"
	@echo "  2. Commit changes: git add . && git commit -m 'Update MN-DOC & KG'"
	@echo ""

# ─────────────────────────────────────────────────────────────────────────────
# Check for Drift (CI use)
# ─────────────────────────────────────────────────────────────────────────────
check-drift: all-kg
	@echo "🔍 Checking for drift in generated files..."
	@if git diff --quiet $(MNDOC_OUTPUT) $(KG_OUTPUT) 2>/dev/null; then \
		echo "✅ Generated files are up-to-date"; \
	else \
		echo "❌ Generated files have drifted from source!"; \
		echo ""; \
		echo "The following files need to be regenerated and committed:"; \
		git diff --name-only $(MNDOC_OUTPUT) $(KG_OUTPUT) 2>/dev/null || true; \
		echo ""; \
		echo "Run 'make all-kg' and commit the changes."; \
		exit 1; \
	fi

# ─────────────────────────────────────────────────────────────────────────────
# Clean Generated Files
# ─────────────────────────────────────────────────────────────────────────────
clean-generated:
	@echo "🧹 Removing generated files..."
	rm -f $(MNDOC_OUTPUT) $(KG_OUTPUT) $(SUPERROOT_OUTPUT)
	@echo "✅ Generated files removed"

# ─────────────────────────────────────────────────────────────────────────────
# Reports Analysis
# ─────────────────────────────────────────────────────────────────────────────
analyze-reports:
	@echo "📊 Analyzing root-level reports..."
	$(PYTHON) tools/docs/analyze_root_reports.py \
		--repo-root . \
		--output $(REPORTS_ANALYSIS_MD) \
		--json-output $(REPORTS_ANALYSIS_JSON) \
		--verbose
	@echo "✅ Reports analysis complete!"
	@echo "   - Markdown: $(REPORTS_ANALYSIS_MD)"
	@echo "   - JSON: $(REPORTS_ANALYSIS_JSON)"

# ─────────────────────────────────────────────────────────────────────────────
# Governance Validation
# ─────────────────────────────────────────────────────────────────────────────
validate-governance:
	@echo "🔍 Validating Architecture Governance Matrix..."
	$(PYTHON) tools/governance/validate-governance-matrix.py --verbose

validate-governance-ci:
	@echo "🔍 Validating Architecture Governance Matrix (CI mode)..."
	$(PYTHON) tools/governance/validate-governance-matrix.py

# ─────────────────────────────────────────────────────────────────────────────
# Help
# ─────────────────────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "═══════════════════════════════════════════════════════════════════"
	@echo "           Unmanned Island System - MN-DOC & KG Automation"
	@echo "═══════════════════════════════════════════════════════════════════"
	@echo ""
	@echo "Available targets:"
	@echo ""
	@echo "  make mndoc           Generate MN-DOC from README.md"
	@echo "  make kg              Build Knowledge Graph (includes mndoc)"
	@echo "  make superroot       Project to SuperRoot entities (includes kg)"
	@echo "  make all-kg          Run all generation tasks"
	@echo "  make check-drift     Check if generated files are up-to-date"
	@echo "  make clean-generated Remove all generated YAML files"
	@echo "  make analyze-reports Analyze root-level reports"
	@echo "  make validate-governance     Validate Architecture Governance Matrix"
	@echo "  make validate-governance-ci  Validate governance (CI mode)"
	@echo "  make help            Show this help message"
	@echo ""
	@echo "Source of Truth:"
	@echo "  - README.md, code, config, docs = source"
	@echo "  - generated-mndoc.yaml, knowledge-graph.yaml = build artifacts"
	@echo ""
	@echo "Workflow:"
	@echo "  1. Edit source files (README.md, code, etc.)"
	@echo "  2. Run: make all-kg"
	@echo "  3. Review: git diff"
	@echo "  4. Commit: git add . && git commit"
	@echo ""
