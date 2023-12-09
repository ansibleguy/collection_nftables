#!/usr/bin/env bash

set -eo pipefail

if [ -n "$1" ] && [ -n "$2" ] && [ -n "$3" ] && [ -n "$4" ] && [ -n "$5" ]
then
  export TEST_USER="$1"
  export TEST_PWD="$2"
  export TEST_PORT="$3"
  export TEST_VM="$4"
  export TEST_CONT="$5"
  if [ -f "$TEST_PWD" ]
  then
    TEST_PWD="$(cat "$TEST_PWD")"
  fi
  echo "CONFIG: User '${TEST_USER}', Port '${TEST_PORT}', VM '${TEST_VM}', CONTAINER '${TEST_CONT}'"
fi

cd "$(dirname "$0")/.."
COL_DIR="$(pwd)"
TMP_DIR="/tmp/.nftables_test_$(date +%s)"

TMP_COL_DIR="${TMP_DIR}/collections"
mkdir -p "${TMP_COL_DIR}/ansible_collections/ansibleguy/"
ln -s "$COL_DIR" "${TMP_COL_DIR}/ansible_collections/ansibleguy/nftables"

export ANSIBLE_COLLECTIONS_PATH="$TMP_COL_DIR"
export ANSIBLE_INVENTORY_UNPARSED_WARNING=False

cd "${COL_DIR}/tests/"

ARG_FLAGS=''
for arg in "$@"
do
  if [[ $arg == -* ]]
  then
    ARG_FLAGS="${ARG_FLAGS} ${arg}"
  fi
done
