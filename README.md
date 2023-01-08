# Ansible Collection - ansibleguy.nftables

[![Molecule Test Status](https://badges.ansibleguy.net/collection_nftables.molecule.svg)](https://github.com/ansibleguy/collection_nftables/blob/latest/roles/)
[![YamlLint Test Status](https://badges.ansibleguy.net/collection_nftables.yamllint.svg)](https://yamllint.readthedocs.io/en/stable/)
[![Ansible-Lint Test Status](https://badges.ansibleguy.net/collection_nftables.ansiblelint.svg)](https://ansible-lint.readthedocs.io/en/latest/)
[![Ansible Galaxy](https://img.shields.io/ansible/collection/COLLECTION-ID)](https://galaxy.ansible.com/ansibleguy/nftables)

----

## Requirements

First - install nftables!

For the python library to work the installed NFTables version needs to be >= 0.9.3

```bash
sudo apt install nftables

# check the installed version
sudo apt policy nftables
```

The ansible-modules of this collection use the [python3-nftables module](https://ral-arturo.org/2020/11/22/python-nftables-tutorial.html) to interact with nftables. This interface is already used by [firewalld](https://firewalld.org/2019/09/libnftables-JSON).

You can either install it using your package manager (_apt in the example_) or install it using pip (_unofficial version provided by AnsibleGuy_).

```bash
# package manager
sudo apt install python3-nftables

# pip
pip install ansibleguy-nftables
```


Then - install the collection itself:

```bash
# unstable/latest version:
ansible-galaxy collection install git+https://github.com/ansibleguy/collection_nftables.git

# install to specific director for easier development
cd $PLAYBOOK_DIR
ansible-galaxy collection install git+https://github.com/ansibleguy/collection_nftables.git -p ./collections
```

----

## Usage

See: [Docs](https://github.com/ansibleguy/collection_nftables/blob/latest/Usage.rst)

----

## Modules

not implemented => development => [testing](https://github.com/ansibleguy/collection_nftables/blob/latest/tests) => unstable (_practical testing_) => stable

| Function          | Module                       | Usage                                                                                                                                                                                            | State           |
|:------------------|:-----------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------|
| **Rules**         | ansibleguy.nftables.rule     | [Docs](https://github.com/ansibleguy/collection_nftables/blob/latest/Usage.rst), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes#Rules) | development     |
| **Complex rules** | ansibleguy.nftables.rule_raw | [Docs](https://github.com/ansibleguy/collection_nftables/blob/latest/Usage.rst), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes#Rules) | not implemented |
| **Chains**        | ansibleguy.nftables.chain    | [Docs](https://github.com/ansibleguy/collection_nftables/blob/latest/Usage.rst), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains)                           | not implemented |
| **Tables**        | ansibleguy.nftables.table    | [Docs](https://github.com/ansibleguy/collection_nftables/blob/latest/Usage.rst), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_tables)                           | not implemented |
| **Variables**     | ansibleguy.nftables.var      | [Docs](https://github.com/ansibleguy/collection_nftables/blob/latest/Usage.rst), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Scripting#Defining_variables)                 | not implemented |
| **Sets**          | ansibleguy.nftables.set      | [Docs](https://github.com/ansibleguy/collection_nftables/blob/latest/Usage.rst), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Sets)                                         | not implemented |
| **Limits**        | ansibleguy.nftables.limit    | [Docs](https://github.com/ansibleguy/collection_nftables/blob/latest/Usage.rst), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Limits)                                       | not implemented |
| **Counters**      | ansibleguy.nftables.counter  | [Docs](https://github.com/ansibleguy/collection_nftables/blob/latest/Usage.rst), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Counters)                                     | not implemented |
