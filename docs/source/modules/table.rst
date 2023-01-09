.. _modules_table:

.. include:: ../_include/head.rst

======
Tables
======

**STATE**: development

**TESTS**: `ansibleguy.nftables.table <https://github.com/ansibleguy/collection_nftables/blob/latest/roles/test1/tasks/table.yml>`_

**NFTables Docs**:

* `Documentation on tables <https://wiki.nftables.org/wiki-nftables/index.php/Configuring_tables>`_

----

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.nftables.table
=========================


----

Usage
*****


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
