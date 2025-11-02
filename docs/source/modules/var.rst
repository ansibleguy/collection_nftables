.. _modules_var:

.. include:: ../_include/head.rst

=========
Variables
=========

.. include:: ../_include/dev.rst

**STATE**: development

**TESTS**: `oxlorg.nftables.var <https://github.com/O-X-L/ansible-collection-nftables/blob/latest/roles/_nftables_test1/tasks/var.yml>`_

**NFTables Docs**:

* `Documentation on variables <https://wiki.nftables.org/wiki-nftables/index.php/Scripting#Defining_variables>`_

----

Definition
**********

.. include:: ../_include/param_basic.rst

oxlorg.nftables.var
=======================


Usage
*****


Examples
********

oxlorg.nftables.var
=======================

.. code-block:: yaml

    - hosts: all
      gather_facts: no
      become: true
      tasks:
        - name: Example
          oxlorg.nftables.var:
