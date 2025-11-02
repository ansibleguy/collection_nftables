.. _modules_limit:

.. include:: ../_include/head.rst

======
Limits
======

.. include:: ../_include/dev.rst

**STATE**: development

**TESTS**: `oxlorg.nftables.limit <https://github.com/O-X-L/ansible-collection-nftables/blob/latest/roles/_nftables_test1/tasks/limit.yml>`_

**NFTables Docs**:

* `Documentation on limits <https://wiki.nftables.org/wiki-nftables/index.php/Limits>`_

----

Definition
**********

.. include:: ../_include/param_basic.rst

oxlorg.nftables.limit
=========================

Usage
*****


Examples
********

oxlorg.nftables.limit
=========================

.. code-block:: yaml

    - hosts: all
      gather_facts: no
      become: true
      tasks:
        - name: Example
          oxlorg.nftables.limit:
