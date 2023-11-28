#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.nftables.plugins.module_utils.helper.utils import \
    profiler
from ansible_collections.ansibleguy.nftables.plugins.module_utils.defaults import \
    NFT_MOD_ARGS
from ansible_collections.ansibleguy.nftables.plugins.module_utils.helper.main import \
    diff_remove_empty
from ansible_collections.ansibleguy.nftables.plugins.module_utils.main.chain import \
    Chain


PROFILE = False  # create log to profile time consumption

# DOCUMENTATION = 'https://nftables.ansibleguy.net/en/latest/modules/rule.html'
# EXAMPLES = 'https://nftables.ansibleguy.net/en/latest/modules/rule.html'


def run_module():
    module_args = dict(
        **NFT_MOD_ARGS,
        table=dict(
            type='str', required=True, aliases=['t'],
            description='The name of the table'
        ),
        table_family=dict(
            type='str', required=True, aliases=['table_type', 'table_fam', 'tt', 'tf'],
            choices=['inet', 'ip6', 'ip', 'arp', 'bridge', 'netdev'],
            description='Table type'
        ),
        name=dict(
            type='str', required=True, aliases=['n', 'chain'],
            description='The name of the chain'
        ),
        hook=dict(
            type='str', required=False, aliases=['h'], description='Chain hook',
            choices=['ingress', 'prerouting', 'forward', 'input', 'output', 'postrouting'],
        ),
        policy=dict(
            type='str', required=False, aliases=['p', 'pol', 'implicit'], choices=['accept', 'drop'],
            description='Implicit rule policy to use',
        ),
        type=dict(
            type='str', required=False, aliases=['t'], default='filter',
            choices=['filter', 'nat', 'route'], description='Chain type'
        ),
        priority=dict(
            type='int', required=False, aliases=['p', 'prio'], default=0,
            choices=[-400, -300, -225, -200, -150, -100, 0, 50, 100, 225, 300],
            description='Chain priority'
        ),
        device=dict(
            type='str', required=False, aliases=['dev'],
            description="Device to use if the chains type is 'netdev'",
        ),
        comment=dict(
            type='str', required=False, aliases=['c', 'cmt'],
        ),
    )

    result = dict(
        changed=False,
        diff={
            'before': None,
            'after': None,
        },
        _executed=[],
        _fail_info={},
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    c = Chain(module=module, result=result)

    def process():
        c.check()
        c.process()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='chain.log')
        # log in /tmp/ansibleguy.nftables/

    else:
        process()

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
