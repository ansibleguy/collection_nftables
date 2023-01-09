.. _modules_rule:

.. include:: ../_include/head.rst

=====
Rules
=====

**STATE**: development

**TESTS**: `ansibleguy.nftables.rule <https://github.com/ansibleguy/collection_nftables/blob/latest/roles/test1/tasks/rule.yml>`_ |
`ansibleguy.nftables.rule_raw <https://github.com/ansibleguy/collection_nftables/blob/latest/roles/test1/tasks/rule_raw.yml>`_

**NFTables Docs**:



* `Source-nat <https://wiki.nftables.org/wiki-nftables/index.php/Performing_Network_Address_Translation_(NAT)#Source_NAT>`_
* `Destination-nat <https://wiki.nftables.org/wiki-nftables/index.php/Performing_Network_Address_Translation_(NAT)#Destination_NAT>`_
* `Masquerading <https://wiki.nftables.org/wiki-nftables/index.php/Performing_Network_Address_Translation_(NAT)#Masquerading>`_

----

Definition
**********

.. include:: ../_include/param_basic.rst

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "id","string","true","\-","uid, name, identifier","Unique identifier of the rule. Used to match the configured rules with the existing ones. This id is added at the beginning of the rule's comment field."
    "table","string","false","\-","t, target_table","The name of the table this rule should be inserted into. If only one exists you don't need to provide its name."
    "table_type","string","false","'ip'","tt, target_table_type","One of: 'inet', 'ip6', 'ip', 'arp', 'bridge', 'netdev'. The type of the table this rule should be inserted into."
    "chain","string","true","\-","c, target_chain","The name of the chain this rule should be inserted into."
    "before","string","false","\-","before_id","This rule should be placed before a specific other rule. Provide the unique identifier of the other rule!"
    "after","string","false","\-","after_id","This rule should be placed after a specific other rule. Provide the unique identifier of the other rule!"

ansibleguy.nftables.rule_raw
============================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "rule","string","false for deletion else true","\-","raw, line, content","The raw rule to add to the config"

----

Usage
*****

Rules are identified/matched using an **unique ID**.

You need to provide one for every rule you manage!

That ID is added at the beginning of the rule's comment field. The ID is separated from the comment using a backslash (*\\*) as separator. Because of this that character will be replaced by an underscore (_) if found in the comment field!

----

Examples
********

ansibleguy.nftables.rule_raw
============================

.. code-block:: yaml

    - hosts: all
      gather_facts: no
      become: true
      tasks:
        - name: Example
          ansibleguy.nftables.rule_raw:
            id: 'example_id'
            chain: 'target_chain'
            # table: 'filter'
            # table_type: 'ip'
            rule: 'iifname "lo" accept comment "Allow loopback traffic"'

        - name: Adding rule
          ansibleguy.opnsense.rule_raw:
            id: '11'
            chain: 'input'
            table: 'filter'
            table_type: 'ip'
            rule: 'iifname "lo" accept comment "Allow loopback traffic"'

        - name: Updating
          ansibleguy.opnsense.rule_raw:
            id: '11'
            chain: 'input'
            table: 'filter'
            table_type: 'ip'
            rule: 'iifname "eno1" accept comment "Allow some traffic"'

        - name: Removing
          ansibleguy.opnsense.rule_raw:
            id: '11'
            chain: 'input'
            table: 'filter'
            table_type: 'ip'
            state: absent
