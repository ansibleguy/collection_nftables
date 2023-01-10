.. _modules_chain:

.. include:: ../_include/head.rst

======
Chains
======

.. include:: ../_include/dev.rst

**STATE**: development

**TESTS**: `ansibleguy.nftables.chain <https://github.com/ansibleguy/collection_nftables/blob/latest/roles/_nftables_test1/tasks/chain.yml>`_

**NFTables Docs**:

* `Documentation on chains <https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains>`_

----

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.nftables.chain
=========================


----

Usage
*****


----

Examples
********

ansibleguy.nftables.chain
=========================

.. code-block:: yaml

    - hosts: all
      gather_facts: no
      become: true
      tasks:
        - name: Example
          ansibleguy.nftables.chain:
