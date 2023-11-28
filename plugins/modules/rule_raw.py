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
from ansible_collections.ansibleguy.nftables.plugins.module_utils.main.rule_raw import RuleRaw


PROFILE = False  # create log to profile time consumption

# DOCUMENTATION = 'https://nftables.ansibleguy.net/en/latest/modules/rule.html'
# EXAMPLES = 'https://nftables.ansibleguy.net/en/latest/modules/rule.html'


def run_module():
    module_args = dict(
        **NFT_MOD_ARGS,
        # placement
        **NFT_RULE_MOD_ARGS,
        # actual rule
        rule=dict(
            type='str', required=False, aliases=['raw', 'line', 'content'],
            description='The raw rule to add to the config'
        ),
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        },
        _executed=[],
        _fail_info={},
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    sort_param_lists(module.params)
    rule = RuleRaw(module=module, result=result)

    def process():
        rule.check()
        rule.process()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='rule_raw.log')
        # log in /tmp/ansibleguy.nftables/

    else:
        process()

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
