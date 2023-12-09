#!/usr/bin/env bash

set -eo pipefail

echo ''
echo '##### PREPARING #####'

source "$(dirname "$0")/test_prep.sh"  # shared

echo ''
echo '##### STARTING #####'

echo "EXECUTING: ansible-playbook -i inventory/hosts.yml cleanup.yml ${ARG_FLAGS}"
# shellcheck disable=SC2046
ansible-playbook -i inventory/hosts.yml cleanup.yml $ARG_FLAGS

rm -rf "$TMP_DIR"

echo ''
echo '##### FINISHED #####'
echo ''
