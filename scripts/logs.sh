#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/comum.sh"

ambiente="${1:-}"
componente="${2:-scheduler}"
validar_ambiente "$ambiente"

kubectl -n "$(namespace "$ambiente")" logs "deployment/airflow-$componente" --tail=200
