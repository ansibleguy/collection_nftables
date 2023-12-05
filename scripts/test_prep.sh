#!/usr/bin/env bash

set -eo pipefail

cd "$(dirname "$0")/.."
COL_DIR="$(pwd)"
TMP_DIR="/tmp/.nftables_test_$(date +%s)"

TMP_COL_DIR="${TMP_DIR}/collections"
mkdir -p "${TMP_COL_DIR}/ansible_collections/ansibleguy/"
ln -s "$COL_DIR" "${TMP_COL_DIR}/ansible_collections/ansibleguy/nftables"

export ANSIBLE_COLLECTIONS_PATH="$TMP_COL_DIR"
export ANSIBLE_INVENTORY_UNPARSED_WARNING=False

cd "${COL_DIR}/tests/"
