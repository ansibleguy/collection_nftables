from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.nftables.plugins.module_utils.base import BaseModule


class Table(BaseModule):
    def __init__(self, module: AnsibleModule, result: dict):
        BaseModule.__init__(self=self, module=module, result=result)

    def check(self):
        tables = self.n.ruleset_raw()
        configured = f"{self.p['family']} {self.p['name']}"

        if configured in tables:
            self.exists = True

        if self.p['state'] == 'present' and not self.exists:
            self.r['changed'] = True

        elif self.p['state'] != 'present' and self.exists:
            self.r['changed'] = True

        elif self.p['state'] == 'present':
            self.r['diff']['after'] = dict(
                family=self.p['family'],
                name=self.p['name'],
            )

    def process(self):
        if self.p['state'] == 'present':
            if not self.exists:
                self.create()

        elif self.exists:
            self.delete()

    def create(self):
        self.n.cmd_exec(f"add table {self.p['family']} {self.p['name']}")

    def delete(self):
        if self.p['force']:
            self.n.cmd_exec(f"delete table {self.p['family']} {self.p['name']}")
