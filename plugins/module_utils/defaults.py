from packaging import version

CONFIG = dict(
    path_log='/tmp/ansibleguy.nftables',
    min_version=version.parse('0.9.3'),
)

NFT_MOD_ARGS = dict(
    debug=dict(type='bool', required=False, default=False),
    state=dict(type='str', required=False, choices=['present', 'absent'], default='present'),
)

NFT_RULE_MOD_ARGS = dict(
    id=dict(
        type='str', required=True, aliases=['name', 'identifier', 'uid'],
        description='Unique identifier of the rule. '
                    'Used to match the configured rules with the existing ones. '
                    "This id is added at the beginning of the rule's comment field."
    ),
    table=dict(
        type='str', required=False, aliases=['t', 'target_table'],
        description='The name of the table this rule should be inserted into. '
                    "If only one exists you don't need to provide its name."
    ),
    table_type=dict(
        type='str', required=False, aliases=['tt', 'target_table_type'],
        choices=['inet', 'ip6', 'ip', 'arp', 'bridge', 'netdev'], default='ip',
        description='The type of the table this rule should be inserted into.'
    ),
    chain=dict(
        type='str', required=True, aliases=['c', 'target_chain'],
        description='The name of the chain this rule should be inserted into.'
    ),
    before=dict(
        type='str', required=False, aliases=['before_id'],
        description='This rule should be placed before a specific other rule. '
                    'Provide the unique identifier of the other rule!'
    ),
    after=dict(
        type='str', required=False, aliases=['before_id'],
        description='This rule should be placed after a specific other rule. '
                    'Provide the unique identifier of the other rule!'
    ),
)
