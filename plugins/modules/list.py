#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.nftables.plugins.module_utils.helper.utils import \
    profiler
from ansible_collections.ansibleguy.nftables.plugins.module_utils.defaults import \
    NFT_MOD_ARGS
from ansible_collections.ansibleguy.nftables.plugins.module_utils.nft import NFT

PROFILE = False  # create log to profile time consumption

# DOCUMENTATION = 'https://nftables.ansibleguy.net/en/latest/modules/list.html'
# EXAMPLES = 'https://nftables.ansibleguy.net/en/latest/modules/list.html'


def run_module():
    module_args = dict(
        **NFT_MOD_ARGS,
        target=dict(
            type='str', required=True, aliases=['t', 'tgt'],
            choices=['tables', 'chains', 'rules'],
            description='What elements to list'
        ),  # todo: integrate counters, limits, sets and so on
        filter_tables=dict(
            type='list', elements='str', required=False, aliases=['ft', 'tables'],
            description='Only list chains or rules of these tables',
            default=[],
        ),
        filter_chains=dict(
            type='list', elements='str', required=False, aliases=['fc', 'chains'],
            description='Only list rules of these chains', default=[],
        ),
    )

    result = dict(
        changed=False,
        data={},
        _executed=[],
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    def process():
        n = NFT(module=module, result=result)
        tables = n.ruleset_raw()

        if module.params['target'] == 'tables':
            result['data'] = list(tables.keys())

        else:
            # apply filters
            filtered_1 = {}

            for table_name, chains in tables.items():
                if len(module.params['filter_tables']) > 0:
                    if table_name not in module.params['filter_tables']:
                        continue

                filtered_1[table_name] = chains

            filtered_2 = {}

            for table, chains in filtered_1.items():
                filtered_3 = {}

                for chain_name, chain_data in chains.items():
                    if len(module.params['filter_chains']) > 0:
                        if chain_name not in module.params['filter_chains']:
                            continue

                    filtered_3[chain_name] = chain_data

                filtered_2[table] = filtered_3

            # extract pre-filtered data
            if module.params['target'] == 'chains':
                for table, chains in filtered_2.items():
                    result['data'][table] = list(chains.keys())

            elif module.params['target'] == 'rules':
                result['data'] = filtered_2

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='list.log')
        # log in /tmp/ansibleguy.nftables/

    else:
        process()

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
