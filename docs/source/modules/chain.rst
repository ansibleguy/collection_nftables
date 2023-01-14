.. _modules_chain:

.. include:: ../_include/head.rst

======
Chains
======

.. include:: ../_include/dev.rst

**STATE**: testing

**TESTS**: `ansibleguy.nftables.chain <https://github.com/ansibleguy/collection_nftables/blob/latest/roles/_nftables_test1/tasks/chain.yml>`_

**NFTables Docs**:

* `Documentation on chains <https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains>`_

----

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.nftables.chain
=========================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "table","string","true","\-","t","The name of the table"
    "table_family","string","true","\-","table_type, tt, table_fam, tt","One of: 'inet', 'ip6', 'ip', 'arp', 'bridge', 'netdev'. Table type"
    "name","string","true","\-","n, chain","The name of the chain"
    "hook","string","false","\-","h","One of: 'ingress', 'prerouting', 'forward', 'input', 'output', 'postrouting'. Chain hook"
    "policy","string","false","\-","p, pol, implicit","One of: 'accept', 'drop'. Implicit rule policy to use"
    "type","string","false","filter","t","One of: 'filter', 'nat', 'route'. Chain type"
    "priority","string","false","0","p, prio","One of: -400, -300, -225, -200, -150, -100, 0, 50, 100, 225, 300. Chain priority"
    "device","string","false","\-","dev","Device to use if the chains type is 'netdev'"
    "comment","string","false","\-","c, cmt","\-"

----

Usage
*****

Changes on existing chains must be enforced using the 'force' parameter.

**Be aware**: If a chain changed it needs to be removed and re-added to apply those changes! **All of its rules are be dropped!**

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
            table: 'main'
            table_family: 'ip'
            name: 'example'
            # hook: ''
            # policy: ''
            # type: 'filter'
            # priority: 0
            # device: ''
            # comment: ''
            # force: false
            # state: present

        - name: Adding chain to manage forward-traffic
          ansibleguy.nftables.chain:
            table: 'main'
            table_family: 'ip'
            name: 'example'
            hook: 'forward'
            policy: 'drop'

        - name: Adding comment to chain
          ansibleguy.nftables.chain:
            table: 'main'
            table_family: 'ip'
            name: 'fwd'
            hook: 'forward'
            policy: 'drop'
            comment: 'forwarding traffic'

        - name: Pulling existing chains
          ansibleguy.nftables.list:
            target: 'chains'
          register: chains

        - name: Showing chains
          ansible.builtin.debug:
            var: chains.data

        - name: Adding sub-chain
          ansibleguy.nftables.chain:
            table: 'main'
            table_family: 'ip'
            name: 'sub'
            comment: 'chain used for some special stuff'

        - name: Removing forwarding-chain
          ansibleguy.nftables.chain:
            table: 'main'
            table_family: 'ip'
            name: 'fwd'
            state: absent
            force: true
