.. _usage_basic:

.. include:: ../_include/head.rst

=========
2 - Basic
=========

Documentation
*************

* `Overview <https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes>`_
* `Man Page <https://www.mankier.com/8/nft>`_
* `Ruleset Element definition <https://www.mankier.com/5/libnftables-json#Ruleset_Elements>`_
* `Statement definition <https://www.mankier.com/5/libnftables-json#Statements>`_

----

Basics
******

Running
=======

These modules support check-mode and can show you the difference between existing and configured items:

.. code-block:: bash

    # show differences
    ansible-playbook nftables.yml -D

    # run in check-mode (no changes are made)
    ansible-playbook nftables.yml --check

