.. _modules_limit:

.. include:: ../_include/head.rst

======
Limits
======

.. include:: ../_include/dev.rst

**STATE**: development

**TESTS**: `ansibleguy.nftables.limit <https://github.com/ansibleguy/collection_nftables/blob/latest/roles/_nftables_test1/tasks/limit.yml>`_

**NFTables Docs**:

* `Documentation on limits <https://wiki.nftables.org/wiki-nftables/index.php/Limits>`_

----

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.nftables.limit
=========================


----

Usage
*****


----

Examples
********

ansibleguy.nftables.limit
=========================

.. code-block:: yaml

    - hosts: all
      gather_facts: no
      become: true
      tasks:
        - name: Example
          ansibleguy.nftables.limit:
