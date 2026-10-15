#!/usr/bin/env bash
set -euo pipefail

validar_ambiente() {
  case "${1:-}" in
    dev|hml|prod) ;;
    *) echo "uso: $0 <dev|hml|prod>"; exit 1 ;;
  esac
}

namespace() {
  echo "airflow-$1"
}
