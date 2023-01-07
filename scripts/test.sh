#!/bin/bash

set -e

echo ''

DEBUG=false

if [ -z "$1" ]
then
  echo 'Arguments:'
  echo '  1: path to virtual environment (optional)'
  echo ''
  exit 1
else
  source "$1/bin/activate"
fi

if [[ "$DEBUG" == true ]]
then
  VERBOSITY='-D -vvv'
else
  VERBOSITY=''
fi

cd "$(dirname "$0")/.."
rm -rf "$HOME/.ansible/collections/ansible_collections/ansibleguy/nftables"
ansible-galaxy collection install git+https://github.com/ansibleguy/collection_nftables.git

function run_test() {
  module="$1"
  check_mode="$2"

  echo ''
  echo '##############################'
  echo "RUNNING TESTS of module: '$module'"
  echo ''

  ansible-playbook "tests/$module.yml" --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY
  if [[ "$check_mode" == '1' ]]
  then
    ansible-playbook "tests/$module.yml" --check --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY
  fi
}

echo ''
echo '##############################'
echo 'STARTING TESTS!'
echo '##############################'
echo ''

# run_test 'rule' 1


echo ''
echo '##############################'
echo 'FINISHED TESTS!'
echo '##############################'
echo ''
