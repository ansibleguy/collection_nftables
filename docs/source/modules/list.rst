.. _modules_list:

.. include:: ../_include/head.rst

====
List
====

**STATE**: testing

**TESTS**: `ansibleguy.nftables.list <https://github.com/ansibleguy/collection_nftables/blob/latest/roles/_nftables_test1/tasks/list.yml>`_

----

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.nftables.list
========================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "target","string","true","\-","t, tgt","One of: 'tables', 'chains', 'rules'. What you want to query"
    "filter_tables","list","false","\-","ft, tables","Add the tables you want to query to this list. The table format must be '{family} {name}' as tables can have non-unique names."
    "filter_chains","list","false","\-","fc, chains","Add the chains you want to query to this list."


----

Examples
********

ansibleguy.nftables.list
========================

.. code-block:: yaml

    - hosts: all
      gather_facts: no
      become: true
      tasks:
        - name: Example
          ansibleguy.nftables.list:
            target: 'rules'
            # filter_tables: 'ip filter'
            # filter_chains: 'ufw-not-local'

        - name: Pulling existing tables
          ansibleguy.nftables.list:
            target: 'tables'
          register: nftables_tables

        - name: Show tables
          ansible.builtin.debug:
            var: nftables_tables.data

        # ["ip filter", "ip6 filter"]

        - name: Pulling existing chains of table 'ip filter'
          ansibleguy.nftables.list:
            target: 'chains'
            filter_tables: 'ip filter'  # 'ip' = family, 'filter' = name
          register: nftables_chains

        - name: Show chains
          ansible.builtin.debug:
            var: nftables_chains.data

        # {"ip filter": ["input", "output", "route"]}

        - name: Pulling existing rules of chain 'input' in table 'ip filter'
          ansibleguy.nftables.list:
            target: 'rules'
            filter_tables: 'ip filter'
            filter_chains: 'input'
          register: nftables_rules

        - name: Show rules
          ansible.builtin.debug:
            var: nftables_rules.data

        # {"ip filter": {
        #   "input": [
        #     {"handle": "113", "rule": "fib daddr type local counter packets 0 bytes 0 return"}
        #   ]
        # }}
