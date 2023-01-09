.. _modules_counter:

.. include:: ../_include/head.rst

========
Counters
========

**STATE**: development

**TESTS**: `ansibleguy.nftables.counter <https://github.com/ansibleguy/collection_nftables/blob/latest/roles/test1/tasks/counter.yml>`_

**NFTables Docs**:

* `Documentation on counters <https://wiki.nftables.org/wiki-nftables/index.php/Counters>`_

----

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.nftables.counter
===========================


----

Usage
*****


----

Examples
********

ansibleguy.nftables.counter
===========================

.. code-block:: yaml

    - hosts: all
      gather_facts: no
      become: true
      tasks:
        - name: Example
          ansibleguy.nftables.counter:
