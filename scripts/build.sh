#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

echo ''
echo 'BUILDING tarball'
echo ''

rm -f ansibleguy-nftables-*.tar.gz
ansible-galaxy collection build
