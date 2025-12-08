#!/bin/bash
set -euo pipefail

NAMESPACE="intelligent-hyperautomation-baseline"
BASELINE_DIR="${BASELINE_DIR:-./baselines}"
LOG_FILE="/tmp/baseline-deployment-$(date +%Y%m%d-%H%M%S).log"
ROLLBACK_STACK=()
DRY_RUN="${DRY_RUN:-false}"
SKIP_VALIDATION="${SKIP_VALIDATION:-false}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
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

log_info() {
    echo -e "${CYAN}[$(date +'%Y-%m-%d %H:%M:%S')] ℹ️  $*${NC}" | tee -a "$LOG_FILE"
}

print_banner() {
    echo ""
    echo -e "${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                                                                ║${NC}"
    echo -e "${CYAN}║    ${GREEN}L1 Baseline Automated Deployment System v1.0${CYAN}              ║${NC}"
    echo -e "${CYAN}║    ${YELLOW}Intelligent Hyperautomation Foundation${CYAN}                   ║${NC}"
    echo -e "${CYAN}║                                                                ║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

check_prerequisites() {
    log "Checking prerequisites..."
    
    local missing_tools=()
    
    if ! command -v kubectl &> /dev/null; then
        missing_tools+=("kubectl")
    fi
    
    if ! command -v jq &> /dev/null; then
        log_warning "jq not found. JSON validation will be skipped."
    fi
    
    if ! command -v yq &> /dev/null; then
        log_warning "yq not found. YAML validation will be limited."
    fi
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        log_error "Please install missing tools and try again."
        exit 1
    fi
    
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Cannot connect to Kubernetes cluster."
        log_error "Please check your kubeconfig and cluster availability."
        exit 1
    fi
    
    local k8s_version=$(kubectl version --short 2>/dev/null | grep "Server Version" | awk '{print $3}' | sed 's/v//')
    log_info "Connected to Kubernetes cluster version: $k8s_version"
    
    log_success "Prerequisites check passed"
}

create_namespace() {
    log "Creating namespace: $NAMESPACE"
    
    if kubectl get namespace "$NAMESPACE" &> /dev/null; then
        log_warning "Namespace already exists: $NAMESPACE"
        
        read -p "Do you want to continue with existing namespace? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "Deployment cancelled by user"
            exit 0
        fi
    else
        if [ "$DRY_RUN" = "true" ]; then
            log_info "[DRY-RUN] Would create namespace: $NAMESPACE"
        else
            kubectl create namespace "$NAMESPACE"
            log_success "Namespace created: $NAMESPACE"
        fi
    fi
    
    log "Applying namespace labels and annotations..."
    if [ "$DRY_RUN" = "false" ]; then
        kubectl label namespace "$NAMESPACE" \
            baseline.level=L-A \
            baseline.version=v1.0.0 \
            governance.io/constitutional=true \
            governance.io/layer=L1 \
            --overwrite
        
        kubectl annotate namespace "$NAMESPACE" \
            baseline.io/deployed-at="$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
            baseline.io/deployed-by="$(whoami)@$(hostname)" \
            --overwrite
        
        log_success "Namespace labels and annotations applied"
    fi
}

validate_yaml_file() {
    local file=$1
    
    if [ ! -f "$file" ]; then
        log_error "File not found: $file"
        return 1
    fi
    
    if ! kubectl apply --dry-run=client -f "$file" &> /dev/null; then
        log_error "YAML validation failed for: $file"
        kubectl apply --dry-run=client -f "$file" 2>&1 | tee -a "$LOG_FILE"
        return 1
    fi
    
    return 0
}

deploy_baseline() {
    local baseline_num=$1
    local baseline_name=$2
    local baseline_file="${BASELINE_DIR}/baseline-${baseline_num}-${baseline_name}.yaml"
    local wait_resources=$3
    
    log ""
    log "=================================================="
    log "Deploying Baseline ${baseline_num}: ${baseline_name}"
    log "=================================================="
    
    if [ ! -f "$baseline_file" ]; then
        log_error "Baseline file not found: $baseline_file"
        return 1
    fi
    
    log_info "Validating YAML file..."
    if ! validate_yaml_file "$baseline_file"; then
        return 1
    fi
    log_success "YAML validation passed"
    
    if [ "$DRY_RUN" = "true" ]; then
        log_info "[DRY-RUN] Would deploy: $baseline_file"
        kubectl apply --dry-run=client -f "$baseline_file" | tee -a "$LOG_FILE"
        return 0
    fi
    
    log_info "Applying baseline configuration..."
    if kubectl apply -f "$baseline_file"; then
        log_success "Baseline ${baseline_num} deployed successfully"
        ROLLBACK_STACK+=("$baseline_file")
    else
        log_error "Failed to deploy baseline ${baseline_num}"
        return 1
    fi
    
    if [ -n "$wait_resources" ]; then
        log_info "Waiting for resources to be ready..."
        IFS=',' read -ra RESOURCES <<< "$wait_resources"
        for resource in "${RESOURCES[@]}"; do
            local resource_type="${resource%%/*}"
            local resource_name="${resource##*/}"
            
            log_info "  Waiting for $resource_type/$resource_name..."
            if kubectl wait --for=condition=ready \
                --timeout=300s \
                -n "$NAMESPACE" \
                "$resource_type/$resource_name" &> /dev/null; then
                log_success "  $resource_type/$resource_name is ready"
            else
                log_warning "  Timeout waiting for $resource_type/$resource_name"
            fi
        done
    fi
    
    log_success "Baseline ${baseline_num} deployment completed"
    return 0
}

validate_baseline_health() {
    local baseline_num=$1
    local health_checks=$2
    
    if [ "$SKIP_VALIDATION" = "true" ]; then
        log_info "Skipping health validation (SKIP_VALIDATION=true)"
        return 0
    fi
    
    log_info "Running health checks for Baseline ${baseline_num}..."
    
    IFS=',' read -ra CHECKS <<< "$health_checks"
    for check in "${CHECKS[@]}"; do
        local resource_type="${check%%/*}"
        local resource_name="${check##*/}"
        
        if kubectl get "$resource_type" "$resource_name" -n "$NAMESPACE" &> /dev/null; then
            log_success "  ✓ $resource_type/$resource_name exists"
        else
            log_error "  ✗ $resource_type/$resource_name not found"
            return 1
        fi
    done
    
    log_success "Health checks passed for Baseline ${baseline_num}"
    return 0
}

rollback_deployment() {
    log_error "Deployment failed. Initiating rollback..."
    
    local rollback_count=${#ROLLBACK_STACK[@]}
    if [ $rollback_count -eq 0 ]; then
        log_warning "Nothing to rollback"
        return
    fi
    
    log_warning "Rolling back $rollback_count baseline(s)..."
    
    for ((i=${#ROLLBACK_STACK[@]}-1; i>=0; i--)); do
        local file="${ROLLBACK_STACK[$i]}"
        log_info "  Rolling back: $file"
        
        if kubectl delete -f "$file" --ignore-not-found=true; then
            log_success "  Rolled back: $file"
        else
            log_error "  Failed to rollback: $file"
        fi
    done
    
    log_warning "Rollback completed"
}

deploy_all_baselines() {
    log "Starting sequential baseline deployment..."
    log ""
    
    if ! deploy_baseline 1 "namespace-governance" ""; then
        log_error "Failed to deploy Baseline 1"
        rollback_deployment
        exit 1
    fi
    
    if ! validate_baseline_health 1 "configmap/namespace-governance-policy,configmap/capability-registry-schema"; then
        log_error "Baseline 1 health check failed"
        rollback_deployment
        exit 1
    fi
    
    sleep 5
    
    if ! deploy_baseline 2 "security-rbac" ""; then
        log_error "Failed to deploy Baseline 2"
        rollback_deployment
        exit 1
    fi
    
    if ! validate_baseline_health 2 "configmap/security-baseline-policy,serviceaccount/security-policy-enforcer"; then
        log_error "Baseline 2 health check failed"
        rollback_deployment
        exit 1
    fi
    
    sleep 5
    
    if ! deploy_baseline 3 "resource-management" ""; then
        log_error "Failed to deploy Baseline 3"
        rollback_deployment
        exit 1
    fi
    
    if ! validate_baseline_health 3 "resourcequota/baseline-resource-quota,limitrange/baseline-limit-range"; then
        log_error "Baseline 3 health check failed"
        rollback_deployment
        exit 1
    fi
    
    sleep 5
    
    if ! deploy_baseline 4 "network-policy" ""; then
        log_error "Failed to deploy Baseline 4"
        rollback_deployment
        exit 1
    fi
    
    if ! validate_baseline_health 4 "networkpolicy/baseline-default-deny-all,networkpolicy/baseline-allow-dns"; then
        log_error "Baseline 4 health check failed"
        rollback_deployment
        exit 1
    fi
    
    sleep 5
    
    if ! deploy_baseline 5 "compliance-attestation" ""; then
        log_error "Failed to deploy Baseline 5"
        rollback_deployment
        exit 1
    fi
    
    if ! validate_baseline_health 5 "configmap/compliance-framework-baseline,cronjob/compliance-attestation-job"; then
        log_error "Baseline 5 health check failed"
        rollback_deployment
        exit 1
    fi
    
    sleep 5
    
    if ! deploy_baseline 6 "quantum-orchestration" ""; then
        log_error "Failed to deploy Baseline 6"
        rollback_deployment
        exit 1
    fi
    
    if ! validate_baseline_health 6 "configmap/quantum-orchestration-baseline,service/quantum-orchestration-service"; then
        log_error "Baseline 6 health check failed"
        rollback_deployment
        exit 1
    fi
    
    log_success "All baselines deployed successfully!"
}

generate_deployment_report() {
    log ""
    log "=================================================="
    log "         DEPLOYMENT SUMMARY REPORT"
    log "=================================================="
    log ""
    log "Namespace: $NAMESPACE"
    log "Deployment Time: $(date)"
    log "Deployed By: $(whoami)@$(hostname)"
    log "Log File: $LOG_FILE"
    log ""
    
    log "Deployed Baselines:"
    log "  [1] Namespace Governance Foundation"
    log "  [2] Security & RBAC Foundation"
    log "  [3] Resource Quotas & Limits Foundation"
    log "  [4] Network Policy Foundation"
    log "  [5] Compliance & Attestation Foundation"
    log "  [6] Quantum-Enabled Orchestration Foundation"
    log ""
    
    log "Namespace Resources:"
    kubectl get all -n "$NAMESPACE" 2>/dev/null | tee -a "$LOG_FILE"
    log ""
    
    log "ConfigMaps:"
    kubectl get configmap -n "$NAMESPACE" 2>/dev/null | tee -a "$LOG_FILE"
    log ""
    
    log "Network Policies:"
    kubectl get networkpolicy -n "$NAMESPACE" 2>/dev/null | tee -a "$LOG_FILE"
    log ""
    
    log "Resource Quotas:"
    kubectl get resourcequota -n "$NAMESPACE" 2>/dev/null | tee -a "$LOG_FILE"
    log ""
    
    log_success "Deployment completed successfully!"
    log ""
    log "Next Steps:"
    log "  1. Run validation: ./validate-all-baselines.sh"
    log "  2. Review logs: cat $LOG_FILE"
    log "  3. Monitor namespace: kubectl get all -n $NAMESPACE -w"
    log "  4. Check compliance: kubectl get cronjob compliance-attestation-job -n $NAMESPACE"
    log ""
}

show_usage() {
    cat <<EOF
Usage: $0 [OPTIONS]

Deploy L1 Constitutional Baselines to Kubernetes cluster.

Options:
    --dry-run              Perform a dry-run without applying changes
    --skip-validation      Skip health validation checks
    --baseline-dir DIR     Directory containing baseline YAML files (default: ./baselines)
    --namespace NS         Target namespace (default: intelligent-hyperautomation-baseline)
    --help                 Show this help message

Environment Variables:
    DRY_RUN                Set to 'true' for dry-run mode
    SKIP_VALIDATION        Set to 'true' to skip validation
    BASELINE_DIR           Directory containing baseline files

Examples:
    # Normal deployment
    $0

    # Dry-run mode
    $0 --dry-run

    # Custom baseline directory
    $0 --baseline-dir /path/to/baselines

    # Skip validation (faster, but not recommended)
    $0 --skip-validation

EOF
}

parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN="true"
                shift
                ;;
            --skip-validation)
                SKIP_VALIDATION="true"
                shift
                ;;
            --baseline-dir)
                BASELINE_DIR="$2"
                shift 2
                ;;
            --namespace)
                NAMESPACE="$2"
                shift 2
                ;;
            --help)
                show_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
}

main() {
    parse_arguments "$@"
    
    print_banner
    
    log "Deployment Configuration:"
    log "  Namespace: $NAMESPACE"
    log "  Baseline Directory: $BASELINE_DIR"
    log "  Dry Run: $DRY_RUN"
    log "  Skip Validation: $SKIP_VALIDATION"
    log "  Log File: $LOG_FILE"
    log ""
    
    if [ "$DRY_RUN" = "false" ]; then
        read -p "Do you want to proceed with deployment? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "Deployment cancelled by user"
            exit 0
        fi
    fi
    
    check_prerequisites
    create_namespace
    deploy_all_baselines
    
    if [ "$DRY_RUN" = "false" ]; then
        generate_deployment_report
    else
        log_info "[DRY-RUN] Deployment simulation completed"
    fi
}

trap 'log_error "Deployment interrupted. Rolling back..."; rollback_deployment; exit 1' INT TERM

main "$@"