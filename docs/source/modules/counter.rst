.. _modules_counter:

.. include:: ../_include/head.rst

========
Counters
========

.. include:: ../_include/dev.rst

**STATE**: development

**TESTS**: `oxlorg.nftables.counter <https://github.com/O-X-L/ansible-collection-nftables/blob/latest/roles/_nftables_test1/tasks/counter.yml>`_

**NFTables Docs**:

* `Documentation on counters <https://wiki.nftables.org/wiki-nftables/index.php/Counters>`_

----

Definition
**********

.. include:: ../_include/param_basic.rst

oxlorg.nftables.counter
===========================


Usage
*****


Examples
********

oxlorg.nftables.counter
===========================

.. code-block:: yaml

    - hosts: all
      gather_facts: no
      become: true
      tasks:
        - name: Example
          oxlorg.nftables.counter:
