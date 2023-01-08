==========================
NFTables - Ansible modules
==========================

NFTables
********

For in-depth information on how to use NFTables - see:

* [Overview](https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes)
* [Man Page](https://www.mankier.com/8/nft)
* [Ruleset Element definition](https://www.mankier.com/5/libnftables-json#Ruleset_Elements)
* [Statement definition](https://www.mankier.com/5/libnftables-json#Statements)

Modules
*******

ansibleguy.nftables.rule
========================

ansibleguy.nftables.rule_raw
============================

Usage
*****

Execution
=========

You need to run the modules as root to allow them to interact with NFTables!

.. code-block:: bash

    ansible-playbook --become --ask-pass --diff playbook.yml

    # or the short version
    ansible-playbook -b -K -D playbook.yml

Rules
=====

Definitions
-----------

**NAT**

* `Documentation on source-nat<https://wiki.nftables.org/wiki-nftables/index.php/Performing_Network_Address_Translation_(NAT)#Source_NAT>`_
* `Documentation on destination-nat<https://wiki.nftables.org/wiki-nftables/index.php/Performing_Network_Address_Translation_(NAT)#Destination_NAT>`_
* `Documentation on masquerading<https://wiki.nftables.org/wiki-nftables/index.php/Performing_Network_Address_Translation_(NAT)#Masquerading>`_

**Limits**

`Documentation on limits<https://wiki.nftables.org/wiki-nftables/index.php/Limits>`_


**Counters**

`Documentation on counters<https://wiki.nftables.org/wiki-nftables/index.php/Counters>`_




ansibleguy.nftables.rule
------------------------

ansibleguy.nftables.rule_raw
----------------------------


Troubleshooting
***************


