#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/comum.sh"

ambiente="${1:-}"
validar_ambiente "$ambiente"
ns="$(namespace "$ambiente")"

for componente in scheduler dag-processor api-server triggerer; do
  if kubectl -n "$ns" get deployment "airflow-$componente" >/dev/null 2>&1; then
    kubectl -n "$ns" rollout restart "deployment/airflow-$componente"
    kubectl -n "$ns" rollout status "deployment/airflow-$componente" --timeout=5m
  fi
done

echo "componentes reiniciados em $ambiente"
