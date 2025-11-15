# Ansible Collection - oxlorg.nftables

<p align="center">
    <a title="Support this Project (Donate, Support-Licenses)" href="https://shop.oxl.app/collections/open-source">
        <img src="https://files.oxl.at/img/badge-oss-support.svg" alt="Support Badge (Donate, Support-Licenses)"/>
    </a>
</p>

----

[![Ansible Galaxy](https://badges.oss.oxl.app/galaxy.badge.svg)](https://galaxy.ansible.com/ui/repo/published/oxlorg/nftables)

[![Lint](https://github.com/O-X-L/ansible-collection-nftables/actions/workflows/lint.yml/badge.svg)](https://github.com/O-X-L/ansible-collection-nftables/actions/workflows/lint.yml)
[![Unit Tests](https://github.com/O-X-L/ansible-collection-nftables/actions/workflows/test.yml/badge.svg)](https://github.com/O-X-L/ansible-collection-nftables/actions/workflows/test.yml)

**Functional Tests**: 

* Status: [![Functional Test Status](https://badges.oss.oxl.app/oxlorg.nftables.collection.test.svg)](https://github.com/O-X-L/ansible-collection-nftables/blob/latest/scripts/test.sh) |
[![Functional-Tests](https://github.com/O-X-L/ansible-collection-nftables/actions/workflows/functional_test_result.yml/badge.svg)](https://github.com/O-X-L/ansible-collection-nftables/actions/workflows/functional_test_result.yml)
* Logs: [API](https://ci.oss.oxl.app/api/job/ansible-test-collection-nftables/logs?token=2b7bba30-9a37-4b57-be8a-99e23016ce70&lines=1000) |
[Daily Archive](https://github.com/O-X-L/ansible-collection-nftables/actions/workflows/functional_test_result.yml) |
[Short](https://badges.oss.oxl.app/log/collection_oxlorg.nftables_test_short.log) | [Full](https://badges.oss.oxl.app/log/collection_oxlorg.nftables_test.log)

Internal CI: [Tester Role](https://github.com/O-X-L/ansible-role-oxl-cicd) | [Jobs API](https://github.com/O-X-L/github-self-hosted-jobs-systemd)


----

## Usage

See: [Docs](https://ansible-nftables.oxl.app)

[![Docs Uptime](https://status.oxl.at/api/v1/endpoints/1--oxl_nftables-ansible-collection-docs/uptimes/7d/badge.svg)](https://status.oxl.at/endpoints/1--oxl_nftables-ansible-collection-docs)

[Alternative Link](https://nftables-ansible.readthedocs.io/)

You want a simple Ansible GUI? Check-out our [Ansible WebUI](https://github.com/O-X-L/ansible-webui)

----

## Contribute

Feel free to contribute to this project using [pull-requests](https://github.com/O-X-L/ansible-collection-nftables/pulls), [issues](https://github.com/O-X-L/ansible-collection-nftables/issues) and [discussions](https://github.com/O-X-L/ansible-collection-nftables/discussions)!

See also: [Contributing](https://github.com/O-X-L/ansible-collection-nftables/blob/latest/CONTRIBUTING.md)

----

## Advertisement

* You want a simple **Ansible GUI**?

  Check-out this [Ansible WebUI](https://github.com/O-X-L/ansible-webui)

----

## Modules

not implemented => development => [testing](https://github.com/O-X-L/ansible-collection-nftables/blob/latest/tests) => unstable (_practical testing_) => stable

| Function            | Module                       | Usage                                                                                                                                                                                | State           |
|:--------------------|:-----------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------|
| **Listing**         | oxlorg.nftables.list     | [Docs](https://ansible-nftables.oxl.app/modules/list.html)                                                                                                                  | testing     |
| **Rules**           | oxlorg.nftables.rule     | [Docs](https://ansible-nftables.oxl.app/modules/rule.html), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes#Rules) | development     |
| **1-to-1 Rules**    | oxlorg.nftables.rule_raw | [Docs](https://ansible-nftables.oxl.app/modules/rule.html), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes#Rules) | testing         |
| **Chains**          | oxlorg.nftables.chain    | [Docs](https://ansible-nftables.oxl.app/modules/chain.html), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains)                          | testing |
| **Tables**          | oxlorg.nftables.table    | [Docs](https://ansible-nftables.oxl.app/modules/table.html), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_tables)                          | testing |
| **Variables**       | oxlorg.nftables.var      | [Docs](https://ansible-nftables.oxl.app/modules/var.html), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Scripting#Defining_variables)                  | not implemented |
| **Sets**            | oxlorg.nftables.set      | [Docs](https://ansible-nftables.oxl.app/modules/set.html), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Sets)                                          | not implemented |
| **Limits**          | oxlorg.nftables.limit    | [Docs](https://ansible-nftables.oxl.app/modules/limit.html), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Limits)                                      | not implemented |
| **Counters**        | oxlorg.nftables.counter  | [Docs](https://ansible-nftables.oxl.app/modules/counter.html), [NFTables Docs](https://wiki.nftables.org/wiki-nftables/index.php/Counters)                                  | not implemented |

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

You can either install it using your package manager (_apt in the example_) or using pip (_[unofficial version provided by OXL](https://github.com/O-X-L/python3-nftables)_) on the target system.

```bash
# package manager
sudo apt install python3-nftables

# pip => make sure it is installed for the root user or use a virtualenv
sudo pip install oxl-libnftables
```

You might want to install it using Ansible:

```yaml
- name: Installing NFTables
  ansible.builtin.package:
    name: ['nftables']  # or ['nftables', 'python3-nftables']

- name: Installing NFTables python-module
  ansible.builtin.pip:
    name: 'oxl-libnftables'

- name: Enabling and starting NFTables
  ansible.builtin.service:
    name: 'nftables.service'
    state: started
    enabled: true
```

Then - install the collection itself: (_on the controller_)

```bash
# unstable/latest version:
ansible-galaxy collection install oxlorg.nftables
## OR
ansible-galaxy collection install git+https://github.com/O-X-L/ansible-collection-nftables.git

# install to specific director for easier development
cd $PLAYBOOK_DIR
ansible-galaxy collection install git+https://github.com/O-X-L/ansible-collection-nftables.git -p ./collections
```
