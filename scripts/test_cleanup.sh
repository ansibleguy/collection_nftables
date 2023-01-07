#!/bin/bash

set -e

echo ''

if [ -z "$1" ]
then
  echo 'Arguments:'
  echo '  1: path to virtual environment (optional)'
  echo ''
  exit 1
else
  source "$1/bin/activate"
fi

cd "$(dirname "$0")/.."
rm -rf "$HOME/.ansible/collections/ansible_collections/ansibleguy/nftables"
ansible-galaxy collection install git+https://github.com/ansibleguy/collection_nftables.git

echo ''
echo 'RUNNING CLEANUP'
echo ''

ansible-playbook tests/cleanup.yml --extra-vars="ansible_python_interpreter=$(which python)"

rm -rf "$HOME/.ansible/collections/ansible_collections/ansibleguy/nftables"

echo ''
echo 'FINISHED CLEANUP!'
echo ''
