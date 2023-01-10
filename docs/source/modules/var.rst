.. _modules_var:

.. include:: ../_include/head.rst

=========
Variables
=========

.. include:: ../_include/dev.rst

**STATE**: development

**TESTS**: `ansibleguy.nftables.var <https://github.com/ansibleguy/collection_nftables/blob/latest/roles/_nftables_test1/tasks/var.yml>`_

**NFTables Docs**:

* `Documentation on variables <https://wiki.nftables.org/wiki-nftables/index.php/Scripting#Defining_variables>`_

----

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.nftables.var
=======================


----

Usage
*****


----

Examples
********

ansibleguy.nftables.var
=======================

.. code-block:: yaml

    - hosts: all
      gather_facts: no
      become: true
      tasks:
        - name: Example
          ansibleguy.nftables.var:
