#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.nftables.plugins.module_utils.helper.utils import \
    profiler
from ansible_collections.ansibleguy.nftables.plugins.module_utils.defaults import \
    NFT_MOD_ARGS, NFT_RULE_MOD_ARGS
from ansible_collections.ansibleguy.nftables.plugins.module_utils.helper.main import \
    diff_remove_empty, sort_param_lists
from ansible_collections.ansibleguy.nftables.plugins.module_utils.helper.rule import \
    clean_comment
from ansible_collections.ansibleguy.nftables.plugins.module_utils.main.rule import Rule
from ansible_collections.ansibleguy.nftables.plugins.module_utils.nft import NFT
from ansible_collections.ansibleguy.nftables.plugins.module_utils.definition.hc import \
    RULE_ACTIONS

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://nftables.ansibleguy.net/en/latest/modules/rule.html'
EXAMPLES = 'https://nftables.ansibleguy.net/en/latest/modules/rule.html'


def run_module():
    module_args = dict(
        **NFT_MOD_ARGS,
        # placement
        **NFT_RULE_MOD_ARGS,
        # actual rule
        src=dict(
            type='list', elements='str', required=False, aliases=['source', 'source_net'],
        ),
        dest=dict(
            type='list', elements='str', required=False, aliases=['target', 'destination', 'destination_net'],
        ),
        src_port=dict(
            type='list', elements='str', required=False, aliases=['sport', 'source_port'],
        ),
        dest_port=dict(
            type='list', elements='str', required=False, aliases=['port', 'dport', 'destination_port'],
        ),
        proto=dict(
            type='list', elements='str', required=False, aliases=['protocol'],
        ),
        proto_type=dict(
            type='list', elements='str', required=False, aliases=['type', 'protocol_type'],
        ),
        proto_code=dict(
            type='list', elements='str', required=False, aliases=['code', 'protocol_code'],
        ),
        input_int=dict(
            type='list', elements='str', required=False, aliases=['iif', 'iifname', 'input_interface'],
        ),
        output_int=dict(
            type='list', elements='str', required=False, aliases=['oif', 'oifname', 'output_interface'],
        ),
        comment=dict(
            type='str', required=False, aliases=['c', 'cmt'],
        ),
        # what should be done on a match
        action=dict(
            type='str', required=False, aliases=['a', 'do', 'policy'],
            choises=RULE_ACTIONS,
        ),
        src_nat=dict(
            type='str', required=False, aliases=['snat', 'source_nat', 'outbound_nat'],
            description='If a value is provided, it will be used as source-nat target. '
                        'See also: https://wiki.nftables.org/wiki-nftables/index.php/'
                        'Performing_Network_Address_Translation_(NAT)#Source_NAT'
        ),
        dest_nat=dict(
            type='str', required=False, aliases=['dnat', 'destination_nat'],
            description='If a value is provided, it will be used as destination-nat target. '
                        'See also: https://wiki.nftables.org/wiki-nftables/index.php/'
                        'Performing_Network_Address_Translation_(NAT)#Destination_NAT'
        ),
        masquerade=dict(
            type='bool', required=False, aliases=['masque'], default=False,
            description='If set to true source-nat will be performed and its source address '
                        'is automagically set to the address of the output interface. '
                        'See also: https://wiki.nftables.org/wiki-nftables/index.php/'
                        'Performing_Network_Address_Translation_(NAT)#Masquerading'
        ),
        # additional functionality
        limit=dict(
            type='str', required=False, aliases=['lim', 'l'],
            description='Provide a limit or name of a pre-defined limit. '
                        'See also: https://wiki.nftables.org/wiki-nftables/index.php/Limits'
        ),
        counter=dict(
            type='str', required=False, aliases=['lim', 'l'],
            description='If set to true - a counter will be enabled. '
                        'If a string is provided it will link to a pre-defined counter. '
                        'See also: https://wiki.nftables.org/wiki-nftables/index.php/Counters'
        ),
        # src, dest, proto, type, code, iif, oif, dport, sport, counter, limit, action, comment
        # snat, dnat, masque
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        },
        executed=[],
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    sort_param_lists(module.params)
    module.params['comment'] = clean_comment(module.params['comment'])
    n = NFT(module=module, result=result)
    n.parse_ruleset()
    # for t in n.rules[0].matches:
    #     raise SystemExit(t.__dict__)

    # code or type

    rule = Rule(module=module, result=result)

    def process():
        rule.check()
        rule.process()
        if result['changed'] and module.params['reload']:
            rule.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='rule.log')
        # log in /tmp/ansibleguy.nftables/

    else:
        process()

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
