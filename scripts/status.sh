#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/comum.sh"

ambiente="${1:-}"
validar_ambiente "$ambiente"
ns="$(namespace "$ambiente")"

kubectl -n "$ns" get pods -o wide
echo
helm list -n "$ns"
