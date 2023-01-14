from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.nftables.plugins.module_utils.base import BaseModule

from ansible_collections.ansibleguy.nftables.plugins.module_utils.helper.main import \
    one_in, is_in


class Chain(BaseModule):
    PRIO_MAPPING = {
        'filter': 0,
    }

    def __init__(self, module: AnsibleModule, result: dict):
        BaseModule.__init__(self=self, module=module, result=result)

    def check(self):
        if self.p['hook'] is not None:
            if self.p['table_family'] != 'netdev' and self.p['policy'] is None:
                self.m.fail_json(
                    "You need to supply a 'policy' to create a chain that uses a 'hook'."
                )

        prefix = f"{self.p['table_family']} {self.p['table']} {self.p['name']}"
        table = f"{self.p['table_family']} {self.p['table']}"
        configured = self._build_configured(prefix=prefix)

        # check if exists
        tables = self.n.ruleset_raw()

        if table in tables and self.p['name'] in tables[table]:
            self.exists = True

            self.existing = self._build_existing(
                tables=tables,
                table=table,
                prefix=prefix,
            )

        # check if changed
        if self.p['state'] == 'present':
            self.r['diff']['after'] = configured

        self.r['diff']['before'] = self.existing
        self.r['changed'] = self.r['diff']['before'] != self.r['diff']['after']

    def _build_existing(self, tables: dict, table: str, prefix: str) -> str:
        chain_lines = tables[table][self.p['name']]

        if len(chain_lines) > 0:
            chain = None

            if one_in(find=['policy', 'hook', 'priority'], data=chain_lines[0]['rule']):
                chain = chain_lines[0]['rule']

            elif one_in(find=['policy', 'hook', 'priority'], data=chain_lines[1]['rule']):
                chain = chain_lines[1]['rule']
                if is_in('comment', chain_lines[0]['rule']):
                    chain += f" {chain_lines[0]['rule']};"

            if chain is not None:
                for run, cnf in self.PRIO_MAPPING.items():
                    chain = chain.replace(f'priority {run}', f'priority {cnf}')

                return f"{prefix} {{ {chain} }}"

        return prefix

    def _build_configured(self, prefix: str) -> str:
        settings = ''

        if self.p['hook'] is not None:
            settings = ' '.join([f'{f} {self.p[f]}' for f in ['type', 'hook', 'priority']])

        if self.p['table_family'] != 'netdev':
            if settings != '':
                settings += '; '

            if self.p['hook'] is not None and self.p['policy'] is not None:
                settings += f"policy {self.p['policy']}"

        elif self.p['device'] is not None:
            settings += f"device {self.p['device']}"

        if self.p['comment'] is not None:
            settings += f"; comment \"{self.p['comment']}\""

        if settings == '':
            return prefix

        return f"{prefix} {{ {settings}; }}"

    def process(self):
        if self.p['state'] == 'present':
            if not self.exists:
                self.create()

            elif self.r['changed']:
                self.update()

        elif self.exists:
            self.delete()

    def create(self):
        self.n.cmd_exec(f"add chain {self.r['diff']['after']}")

    def delete(self):
        if self.p['force']:
            self.n.cmd_exec(
                f"delete chain {self.p['table_family']} {self.p['table']} {self.p['name']}"
            )

    def update(self):
        if self.p['force']:
            self.delete()
            self.create()
