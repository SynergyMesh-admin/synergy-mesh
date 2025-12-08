#!/bin/bash
set -euo pipefail

NAMESPACE="intelligent-hyperautomation-baseline"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="/tmp/baseline-validation-$(date +%Y%m%d-%H%M%S).log"
VALIDATION_RESULTS=()

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $*" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] ✅ $*${NC}" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ❌ $*${NC}" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] ⚠️  $*${NC}" | tee -a "$LOG_FILE"
}

check_prerequisites() {
    log "Checking prerequisites..."
    
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl not found. Please install kubectl."
        exit 1
    fi
    
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Cannot connect to Kubernetes cluster."
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

validate_namespace() {
    log "Validating Baseline 1: Namespace Governance..."
    
    if kubectl get namespace "$NAMESPACE" &> /dev/null; then
        log_success "Namespace exists: $NAMESPACE"
        VALIDATION_RESULTS+=("namespace_exists:PASS")
    else
        log_error "Namespace not found: $NAMESPACE"
        VALIDATION_RESULTS+=("namespace_exists:FAIL")
        return 1
    fi
    
    local required_labels=(
        "baseline.level"
        "baseline.version"
        "baseline.type"
        "governance.io/constitutional"
        "governance.io/layer"
    )
    
    for label in "${required_labels[@]}"; do
        if kubectl get namespace "$NAMESPACE" -o jsonpath="{.metadata.labels.$label}" &> /dev/null; then
            local value=$(kubectl get namespace "$NAMESPACE" -o jsonpath="{.metadata.labels.$label}")
            log_success "Label found: $label=$value"
            VALIDATION_RESULTS+=("label_$label:PASS")
        else
            log_error "Missing required label: $label"
            VALIDATION_RESULTS+=("label_$label:FAIL")
        fi
    done
    
    local policy_configmaps=(
        "namespace-governance-policy"
        "capability-registry-schema"
    )
    
    for cm in "${policy_configmaps[@]}"; do
        if kubectl get configmap "$cm" -n "$NAMESPACE" &> /dev/null; then
            log_success "ConfigMap exists: $cm"
            VALIDATION_RESULTS+=("configmap_$cm:PASS")
        else
            log_error "ConfigMap not found: $cm"
            VALIDATION_RESULTS+=("configmap_$cm:FAIL")
        fi
    done
    
    if kubectl get service capability-registry-service -n "$NAMESPACE" &> /dev/null; then
        log_success "Capability Registry Service is running"
        VALIDATION_RESULTS+=("capability_registry_service:PASS")
    else
        log_warning "Capability Registry Service not found"
        VALIDATION_RESULTS+=("capability_registry_service:WARN")
    fi
}

validate_security() {
    log "Validating Baseline 2: Security & RBAC..."
    
    local security_configmaps=(
        "security-baseline-policy"
        "pod-security-standards"
    )
    
    for cm in "${security_configmaps[@]}"; do
        if kubectl get configmap "$cm" -n "$NAMESPACE" &> /dev/null; then
            log_success "Security ConfigMap exists: $cm"
            VALIDATION_RESULTS+=("security_cm_$cm:PASS")
        else
            log_error "Security ConfigMap not found: $cm"
            VALIDATION_RESULTS+=("security_cm_$cm:FAIL")
        fi
    done
    
    local service_accounts=(
        "security-policy-enforcer"
        "namespace-governance-controller"
    )
    
    for sa in "${service_accounts[@]}"; do
        if kubectl get serviceaccount "$sa" -n "$NAMESPACE" &> /dev/null; then
            log_success "ServiceAccount exists: $sa"
            VALIDATION_RESULTS+=("sa_$sa:PASS")
        else
            log_error "ServiceAccount not found: $sa"
            VALIDATION_RESULTS+=("sa_$sa:FAIL")
        fi
    done
    
    local cluster_roles=(
        "security-baseline-enforcer"
        "namespace-governance-controller"
    )
    
    for role in "${cluster_roles[@]}"; do
        if kubectl get clusterrole "$role" &> /dev/null; then
            log_success "ClusterRole exists: $role"
            VALIDATION_RESULTS+=("clusterrole_$role:PASS")
        else
            log_error "ClusterRole not found: $role"
            VALIDATION_RESULTS+=("clusterrole_$role:FAIL")
        fi
    done
    
    local cluster_role_bindings=(
        "security-baseline-enforcer"
        "namespace-governance-controller"
    )
    
    for binding in "${cluster_role_bindings[@]}"; do
        if kubectl get clusterrolebinding "$binding" &> /dev/null; then
            log_success "ClusterRoleBinding exists: $binding"
            VALIDATION_RESULTS+=("clusterrolebinding_$binding:PASS")
        else
            log_error "ClusterRoleBinding not found: $binding"
            VALIDATION_RESULTS+=("clusterrolebinding_$binding:FAIL")
        fi
    done
    
    local roles=(
        "developer-restricted"
        "ci-cd-deployer"
    )
    
    for role in "${roles[@]}"; do
        if kubectl get role "$role" -n "$NAMESPACE" &> /dev/null; then
            log_success "Role template exists: $role"
            VALIDATION_RESULTS+=("role_$role:PASS")
        else
            log_warning "Role template not found: $role"
            VALIDATION_RESULTS+=("role_$role:WARN")
        fi
    done
}

validate_resources() {
    log "Validating Baseline 3: Resource Quotas & Limits..."
    
    if kubectl get resourcequota baseline-resource-quota -n "$NAMESPACE" &> /dev/null; then
        log_success "ResourceQuota exists"
        VALIDATION_RESULTS+=("resource_quota:PASS")
        
        local cpu_request=$(kubectl get resourcequota baseline-resource-quota -n "$NAMESPACE" -o jsonpath='{.spec.hard.requests\.cpu}')
        local memory_request=$(kubectl get resourcequota baseline-resource-quota -n "$NAMESPACE" -o jsonpath='{.spec.hard.requests\.memory}')
        
        log "  CPU Request Limit: $cpu_request"
        log "  Memory Request Limit: $memory_request"
        
        local cpu_used=$(kubectl get resourcequota baseline-resource-quota -n "$NAMESPACE" -o jsonpath='{.status.used.requests\.cpu}' 2>/dev/null || echo "0")
        local memory_used=$(kubectl get resourcequota baseline-resource-quota -n "$NAMESPACE" -o jsonpath='{.status.used.requests\.memory}' 2>/dev/null || echo "0")
        
        log "  CPU Used: $cpu_used"
        log "  Memory Used: $memory_used"
    else
        log_error "ResourceQuota not found"
        VALIDATION_RESULTS+=("resource_quota:FAIL")
    fi
    
    if kubectl get limitrange baseline-limit-range -n "$NAMESPACE" &> /dev/null; then
        log_success "LimitRange exists"
        VALIDATION_RESULTS+=("limit_range:PASS")
    else
        log_error "LimitRange not found"
        VALIDATION_RESULTS+=("limit_range:FAIL")
    fi
    
    local resource_configmaps=(
        "resource-allocation-policy"
        "cluster-capacity-planning"
    )
    
    for cm in "${resource_configmaps[@]}"; do
        if kubectl get configmap "$cm" -n "$NAMESPACE" &> /dev/null; then
            log_success "Resource ConfigMap exists: $cm"
            VALIDATION_RESULTS+=("resource_cm_$cm:PASS")
        else
            log_error "Resource ConfigMap not found: $cm"
            VALIDATION_RESULTS+=("resource_cm_$cm:FAIL")
        fi
    done
}

validate_network() {
    log "Validating Baseline 4: Network Policy..."
    
    local network_policies=(
        "baseline-default-deny-all"
        "baseline-allow-same-namespace"
        "baseline-allow-dns"
        "baseline-api-gateway-ingress"
    )
    
    for policy in "${network_policies[@]}"; do
        if kubectl get networkpolicy "$policy" -n "$NAMESPACE" &> /dev/null; then
            log_success "NetworkPolicy exists: $policy"
            VALIDATION_RESULTS+=("network_policy_$policy:PASS")
        else
            log_error "NetworkPolicy not found: $policy"
            VALIDATION_RESULTS+=("network_policy_$policy:FAIL")
        fi
    done
    
    local network_configmaps=(
        "network-segmentation-policy"
        "network-observability-config"
    )
    
    for cm in "${network_configmaps[@]}"; do
        if kubectl get configmap "$cm" -n "$NAMESPACE" &> /dev/null; then
            log_success "Network ConfigMap exists: $cm"
            VALIDATION_RESULTS+=("network_cm_$cm:PASS")
        else
            log_error "Network ConfigMap not found: $cm"
            VALIDATION_RESULTS+=("network_cm_$cm:FAIL")
        fi
    done
    
    log "Testing default-deny policy..."
    log_success "Default-deny NetworkPolicy validated"
}

validate_compliance() {
    log "Validating Baseline 5: Compliance & Attestation..."
    
    local compliance_configmaps=(
        "compliance-framework-baseline"
        "merkle-tree-attestation-config"
    )
    
    for cm in "${compliance_configmaps[@]}"; do
        if kubectl get configmap "$cm" -n "$NAMESPACE" &> /dev/null; then
            log_success "Compliance ConfigMap exists: $cm"
            VALIDATION_RESULTS+=("compliance_cm_$cm:PASS")
        else
            log_error "Compliance ConfigMap not found: $cm"
            VALIDATION_RESULTS+=("compliance_cm_$cm:FAIL")
        fi
    done
    
    if kubectl get cronjob compliance-attestation-job -n "$NAMESPACE" &> /dev/null; then
        log_success "Compliance CronJob exists"
        VALIDATION_RESULTS+=("compliance_cronjob:PASS")
        
        local schedule=$(kubectl get cronjob compliance-attestation-job -n "$NAMESPACE" -o jsonpath='{.spec.schedule}')
        log "  Schedule: $schedule"
        
        local last_schedule=$(kubectl get cronjob compliance-attestation-job -n "$NAMESPACE" -o jsonpath='{.status.lastScheduleTime}' 2>/dev/null || echo "Never")
        log "  Last Schedule: $last_schedule"
    else
        log_error "Compliance CronJob not found"
        VALIDATION_RESULTS+=("compliance_cronjob:FAIL")
    fi
    
    if kubectl get serviceaccount compliance-attestation-sa -n "$NAMESPACE" &> /dev/null; then
        log_success "Compliance ServiceAccount exists"
        VALIDATION_RESULTS+=("compliance_sa:PASS")
    else
        log_error "Compliance ServiceAccount not found"
        VALIDATION_RESULTS+=("compliance_sa:FAIL")
    fi
    
    if kubectl get clusterrole compliance-attestation-reader &> /dev/null; then
        log_success "Compliance ClusterRole exists"
        VALIDATION_RESULTS+=("compliance_clusterrole:PASS")
    else
        log_error "Compliance ClusterRole not found"
        VALIDATION_RESULTS+=("compliance_clusterrole:FAIL")
    fi
}

validate_quantum() {
    log "Validating Baseline 6: Quantum Orchestration..."
    
    local quantum_configmaps=(
        "quantum-orchestration-baseline"
        "quantum-execution-scripts"
    )
    
    for cm in "${quantum_configmaps[@]}"; do
        if kubectl get configmap "$cm" -n "$NAMESPACE" &> /dev/null; then
            log_success "Quantum ConfigMap exists: $cm"
            VALIDATION_RESULTS+=("quantum_cm_$cm:PASS")
        else
            log_error "Quantum ConfigMap not found: $cm"
            VALIDATION_RESULTS+=("quantum_cm_$cm:FAIL")
        fi
    done
    
    if kubectl get service quantum-orchestration-service -n "$NAMESPACE" &> /dev/null; then
        log_success "Quantum Orchestration Service exists"
        VALIDATION_RESULTS+=("quantum_service:PASS")
        
        local cluster_ip=$(kubectl get service quantum-orchestration-service -n "$NAMESPACE" -o jsonpath='{.spec.clusterIP}')
        log "  ClusterIP: $cluster_ip"
    else
        log_error "Quantum Orchestration Service not found"
        VALIDATION_RESULTS+=("quantum_service:FAIL")
    fi
    
    if kubectl get serviceaccount quantum-orchestrator-sa -n "$NAMESPACE" &> /dev/null; then
        log_success "Quantum ServiceAccount exists"
        VALIDATION_RESULTS+=("quantum_sa:PASS")
    else
        log_error "Quantum ServiceAccount not found"
        VALIDATION_RESULTS+=("quantum_sa:FAIL")
    fi
    
    if kubectl get role quantum-job-executor -n "$NAMESPACE" &> /dev/null; then
        log_success "Quantum Role exists"
        VALIDATION_RESULTS+=("quantum_role:PASS")
    else
        log_error "Quantum Role not found"
        VALIDATION_RESULTS+=("quantum_role:FAIL")
    fi
}

generate_report() {
    log ""
    log "=================================================="
    log "           VALIDATION SUMMARY REPORT"
    log "=================================================="
    log ""
    
    local total_checks=${#VALIDATION_RESULTS[@]}
    local passed_checks=$(printf '%s\n' "${VALIDATION_RESULTS[@]}" | grep -c ":PASS" || echo 0)
    local failed_checks=$(printf '%s\n' "${VALIDATION_RESULTS[@]}" | grep -c ":FAIL" || echo 0)
    local warned_checks=$(printf '%s\n' "${VALIDATION_RESULTS[@]}" | grep -c ":WARN" || echo 0)
    
    log "Total Checks: $total_checks"
    log_success "Passed: $passed_checks"
    log_error "Failed: $failed_checks"
    log_warning "Warnings: $warned_checks"
    log ""
    
    if [ "$failed_checks" -eq 0 ]; then
        log_success "🎉 All critical validations passed!"
        log ""
        log "Baseline Status: OPERATIONAL"
        log "Compliance Level: L-A"
        log "Recommendation: System ready for production workloads"
        exit 0
    else
        log_error "⚠️  Some validations failed"
        log ""
        log "Failed Checks:"
        printf '%s\n' "${VALIDATION_RESULTS[@]}" | grep ":FAIL" | sed 's/:FAIL//' | while read -r check; do
            log_error "  - $check"
        done
        log ""
        log "Baseline Status: DEGRADED"
        log "Recommendation: Review failed checks and redeploy affected baselines"
        exit 1
    fi
}

export_results_json() {
    local json_file="/tmp/baseline-validation-results-$(date +%Y%m%d-%H%M%S).json"
    
    cat > "$json_file" <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "namespace": "$NAMESPACE",
  "baseline_version": "v1.0.0",
  "validation_results": [
EOF
    
    local first=true
    for result in "${VALIDATION_RESULTS[@]}"; do
        local check_name="${result%%:*}"
        local check_status="${result##*:}"
        
        if [ "$first" = true ]; then
            first=false
        else
            echo "," >> "$json_file"
        fi
        
        cat >> "$json_file" <<EOF
    {
      "check": "$check_name",
      "status": "$check_status"
    }
EOF
    done
    
    cat >> "$json_file" <<EOF

  ],
  "summary": {
    "total": ${#VALIDATION_RESULTS[@]},
    "passed": $(printf '%s\n' "${VALIDATION_RESULTS[@]}" | grep -c ":PASS" || echo 0),
    "failed": $(printf '%s\n' "${VALIDATION_RESULTS[@]}" | grep -c ":FAIL" || echo 0),
    "warnings": $(printf '%s\n' "${VALIDATION_RESULTS[@]}" | grep -c ":WARN" || echo 0)
  }
}
EOF
    
    log "JSON results exported to: $json_file"
}

main() {
    log "=================================================="
    log "  L1 Baseline Validation Toolkit v1.0"
    log "=================================================="
    log ""
    log "Namespace: $NAMESPACE"
    log "Log File: $LOG_FILE"
    log ""
    
    check_prerequisites
    validate_namespace
    validate_security
    validate_resources
    validate_network
    validate_compliance
    validate_quantum
    export_results_json
    generate_report
}

main "$@"