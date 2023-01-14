.. _modules_table:

.. include:: ../_include/head.rst

======
Tables
======

.. include:: ../_include/dev.rst

**STATE**: testing

**TESTS**: `ansibleguy.nftables.table <https://github.com/ansibleguy/collection_nftables/blob/latest/roles/_nftables_test1/tasks/table.yml>`_

**NFTables Docs**:

* `Documentation on tables <https://wiki.nftables.org/wiki-nftables/index.php/Configuring_tables>`_

----

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.nftables.table
=========================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","n, table","The name of the table"
    "family","string","true","\-","f, fam, type","One of: 'inet', 'ip6', 'ip', 'arp', 'bridge', 'netdev'. Table type"

----

Usage
*****

Changes on existing tables must be enforced using the 'force' parameter.

**Be aware**: If a table changed it needs to be removed and re-added to apply those changes! **All of its chains and rules are be dropped!**

----

Examples
********

ansibleguy.nftables.table
=========================

.. code-block:: yaml

    - hosts: all
      gather_facts: no
      become: true
      tasks:
        - name: Example
          ansibleguy.nftables.table:
            name: 'example'
            family: 'inet'
            # force: false
            # state: present

        - name: Adding inet table 'test'
          ansibleguy.nftables.table:
            name: 'test'
            family: 'inet'

        - name: Pulling existing tables
          ansibleguy.nftables.list:
            target: 'tables'
          register: tables

        - name: Showing tables
          ansible.builtin.debug:
            var: tables.data

        - name: Removing inet table 'test'
          ansibleguy.nftables.table:
            name: 'test'
            family: 'inet'
            state: absent
            force: true
