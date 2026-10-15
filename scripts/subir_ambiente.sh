#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/comum.sh"

ambiente="${1:-}"
validar_ambiente "$ambiente"
ns="$(namespace "$ambiente")"

kubectl apply -f k8s/namespaces.yaml
"$(dirname "$0")/segredos.sh" "$ambiente"
kubectl -n "$ns" apply -f k8s/oracle.yaml
kubectl -n "$ns" rollout status statefulset/oracle --timeout=15m

echo "ambiente $ambiente pronto para receber o airflow"
