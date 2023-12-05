#!/usr/bin/env bash

set -eo pipefail

echo ''
echo '##### PREPARING #####'

source "$(dirname "$0")/test_prep.sh"  # shared

echo ''
echo '##### STARTING #####'

ansible-playbook -k -K -i inventory/hosts.yml cleanup.yml "$@"

rm -rf "$TMP_DIR"

echo ''
echo '##### FINISHED #####'
echo ''
