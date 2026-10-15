#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/comum.sh"

ambiente="${1:-}"
versao="${2:-}"
validar_ambiente "$ambiente"

if [ -z "$versao" ]; then
  echo "uso: $0 <dev|hml|prod> <versao-da-imagem>"
  exit 1
fi

helm repo add apache-airflow https://airflow.apache.org >/dev/null 2>&1 || true
helm repo update apache-airflow >/dev/null

helm upgrade --install airflow apache-airflow/airflow \
  --namespace "$(namespace "$ambiente")" \
  -f k8s/airflow/valores-base.yaml \
  -f "k8s/airflow/valores-$ambiente.yaml" \
  --set images.airflow.tag="$versao" \
  --wait --timeout 15m

echo "versao $versao publicada em $ambiente"
