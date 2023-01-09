.. _modules_set:

.. include:: ../_include/head.rst

====
Sets
====

**STATE**: development

**TESTS**: `ansibleguy.nftables.set <https://github.com/ansibleguy/collection_nftables/blob/latest/roles/test1/tasks/set.yml>`_

**NFTables Docs**:

* `Documentation on sets <https://wiki.nftables.org/wiki-nftables/index.php/Sets>`_

----

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.nftables.set
=======================


----

Usage
*****


----

Examples
********

ansibleguy.nftables.set
=======================

.. code-block:: yaml

    - hosts: all
      gather_facts: no
      become: true
      tasks:
        - name: Example
          ansibleguy.nftables.set:
