#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.nftables.plugins.module_utils.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.nftables.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.nftables.plugins.module_utils.helper.main import \
        diff_remove_empty, sort_param_lists
    from ansible_collections.ansibleguy.nftables.plugins.module_utils.main.rule import Rule

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://github.com/ansibleguy/collection_nftables/blob/latest/Usage.rst'
EXAMPLES = 'https://github.com/ansibleguy/collection_nftables/blob/latest/Usage.rst'


def run_module():
    module_args = dict(
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

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
