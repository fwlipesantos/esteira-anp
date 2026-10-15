#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/comum.sh"

ambiente="${1:-}"
validar_ambiente "$ambiente"
arquivo=".env.$ambiente"

if [ ! -f "$arquivo" ]; then
  echo "arquivo $arquivo nao encontrado, use o .env.exemplo como base"
  exit 1
fi

kubectl -n "$(namespace "$ambiente")" create secret generic anp-oracle \
  --from-env-file="$arquivo" --dry-run=client -o yaml | kubectl apply -f -

echo "segredo anp-oracle atualizado em $ambiente"
