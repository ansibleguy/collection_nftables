# Ansible Collection - ansibleguy.nftables

[![Lint](https://github.com/ansibleguy/collection_nftables/actions/workflows/lint.yml/badge.svg?branch=latest)](https://github.com/ansibleguy/collection_nftables/actions/workflows/lint.yml)
[![Unit Tests](https://github.com/ansibleguy/collection_nftables/actions/workflows/test.yml/badge.svg)](https://github.com/ansibleguy/collection_nftables/actions/workflows/test.yml)
[![Ansible Galaxy](https://badges.ansibleguy.net/galaxy.badge.svg)](https://galaxy.ansible.com/ui/repo/published/ansibleguy/nftables)
[![Docs](https://readthedocs.org/projects/nftables_ansible/badge/?version=latest&style=flat)](https://nftables.ansibleguy.net)

[![Functional Test Status](https://badges.ansibleguy.net/nftables.collection.test.svg)](https://github.com/ansibleguy/collection_nftables/tree/latest/tests)
[![YamlLint Test Status](https://badges.ansibleguy.net/collection_nftables.yamllint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/yamllint.sh.j2)
[![PyLint Test Status](https://badges.ansibleguy.net/collection_nftables.pylint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/pylint.sh.j2)
[![Ansible-Lint Test Status](https://badges.ansibleguy.net/collection_nftables.ansiblelint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/ansiblelint.sh.j2)

Functional Test Logs: [Short](https://badges.ansibleguy.net/log/collection_nftables_test_short.log), [Full](https://badges.ansibleguy.net/log/collection_nftables_test.log)

----

## Usage

See: [Docs](https://nftables.ansibleguy.net)

----

## Contribute

Feel free to contribute to this project using [pull-requests](https://github.com/ansibleguy/collection_nftables/pulls), [issues](https://github.com/ansibleguy/collection_nftables/issues) and [discussions](https://github.com/ansibleguy/collection_nftables/discussions)!

See also: [Contributing](https://github.com/ansibleguy/collection_nftables/blob/latest/CONTRIBUTING.md)

----

## Modules

not implemented => development => [testing](https://github.com/ansibleguy/collection_nftables/blob/latest/tests) => unstable (_practical testing_) => stable

| Function            | Module                       | Usage                                                                                                                                                                                | State           |
|:--------------------|:-----------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------|
| **Listing**         | ansibleguy.nftables.list     | [Docs](https://nftables.ansibleguy.net/en/latest/modules/list.html)                                                                                                                  | testing     |
| **Rules**           | ansibleguy.nftables.rule     | [Docs](https://nftables.ansibleguy.net/en/latest/modules/rule.html), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes#Rules) | development     |
| **1-to-1 Rules**    | ansibleguy.nftables.rule_raw | [Docs](https://nftables.ansibleguy.net/en/latest/modules/rule.html), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes#Rules) | testing         |
| **Chains**          | ansibleguy.nftables.chain    | [Docs](https://nftables.ansibleguy.net/en/latest/modules/chain.html), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains)                          | testing |
| **Tables**          | ansibleguy.nftables.table    | [Docs](https://nftables.ansibleguy.net/en/latest/modules/table.html), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_tables)                          | testing |
| **Variables**       | ansibleguy.nftables.var      | [Docs](https://nftables.ansibleguy.net/en/latest/modules/var.html), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Scripting#Defining_variables)                  | not implemented |
| **Sets**            | ansibleguy.nftables.set      | [Docs](https://nftables.ansibleguy.net/en/latest/modules/set.html), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Sets)                                          | not implemented |
| **Limits**          | ansibleguy.nftables.limit    | [Docs](https://nftables.ansibleguy.net/en/latest/modules/limit.html), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Limits)                                      | not implemented |
| **Counters**        | ansibleguy.nftables.counter  | [Docs](https://nftables.ansibleguy.net/en/latest/modules/counter.html), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Counters)                                  | not implemented |

----

## Requirements

First - install nftables!

For the python library to work the installed NFTables version needs to be >= 0.9.3

```bash
sudo apt install nftables

# check the installed version
sudo apt policy nftables
```

The ansible-modules of this collection use the [python3-nftables module](https://ral-arturo.org/2020/11/22/python-nftables-tutorial.html) to interact with nftables.

You can either install it using your package manager (_apt in the example_) or using pip (_[unofficial version provided by AnsibleGuy](https://github.com/ansibleguy/python3-nftables)_) on the target system.

```bash
# package manager
sudo apt install python3-nftables

# pip => make sure it is installed for the root user or use a virtualenv
sudo pip install ansibleguy-nftables
```

You might want to install it using Ansible:

```yaml
- name: Installing NFTables
  ansible.builtin.package:
    name: ['nftables']  # or ['nftables', 'python3-nftables']

- name: Installing NFTables python-module
  ansible.builtin.pip:
    name: 'ansibleguy-nftables'

- name: Enabling and starting NFTables
  ansible.builtin.service:
    name: 'nftables.service'
    state: started
    enabled: true
```

Then - install the collection itself: (_on the controller_)

```bash
# unstable/latest version:
ansible-galaxy collection install ansibleguy.nftables
## OR
ansible-galaxy collection install git+https://github.com/ansibleguy/collection_nftables.git

# install to specific director for easier development
cd $PLAYBOOK_DIR
ansible-galaxy collection install git+https://github.com/ansibleguy/collection_nftables.git -p ./collections
```
