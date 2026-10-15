#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/comum.sh"

ambiente="${1:-}"
validar_ambiente "$ambiente"
ns="$(namespace "$ambiente")"

helm history airflow -n "$ns" --max 5
helm rollback airflow -n "$ns" --wait

echo "rollback feito em $ambiente"
