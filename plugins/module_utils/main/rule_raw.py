from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.nftables.plugins.module_utils.base import BaseModule

from ansible_collections.ansibleguy.nftables.plugins.module_utils.nft import NFT
from ansible_collections.ansibleguy.nftables.plugins.module_utils.helper.rule import \
    add_id_to_comment
from ansible_collections.ansibleguy.nftables.plugins.module_utils.definition.hc import \
    ID_SEPARATOR, ID_KEY


class RuleRaw(BaseModule):
    def __init__(self, module: AnsibleModule, result: dict):
        BaseModule.__init__(self=self, module=module, result=result)
        self.exists = False
        self.existing = None
        self.n = NFT(module=module, result=result)

    def check(self):
        tables = self.n.ruleset_raw()

        if self.p['table'] is None:
            tables = list(tables.keys())
            if len(tables) == 0:
                self.m.fail_json('No tables exist!')

            elif len(tables) == 1:
                self.p['table'] = tables[0]

            else:
                self.m.fail_json('Multiple tables exist, but no table name was provided!')

        table_w_type = f"{self.p['table_type']} {self.p['table']}"

        if table_w_type not in tables:
            self.m.fail_json(
                f"Provided table '{self.p['table']}' with type '{self.p['table_type']}' "
                f"does not exist! Existing ones: {', '.join(list(tables.keys()))}"
            )

        table = tables[table_w_type]

        if self.p['chain'] not in table:
            self.m.fail_json(
                f"Provided chain '{self.p['chain']}' does not exist! "
                f"Existing ones: {', '.join(list(table.keys()))}"
            )

        rules = {}

        for entry in table[self.p['chain']]:
            for rule, handle in entry.items():
                if handle is None:
                    continue

                if rule.find(ID_KEY) != -1 and rule.find(ID_SEPARATOR) != -1 and rule.find('comment') != -1:
                    # only try to match rules managed by the modules
                    # beginning, uid, comment, end = self._split_beg_uid_comment_end(raw=rule)
                    split_rule = self._split_beg_uid_comment_end(raw=rule)
                    rule_new = f"{split_rule['beg']}comment \"{split_rule['cmt']}\"{split_rule['end']}"
                    rules[split_rule['id']] = {'rule': rule_new, 'handle': handle}

        if self.p['id'] in rules:
            self.exists = True
            self.existing = rules[self.p['id']]['handle']
            rule = rules[self.p['id']]

            if self.p['rule'] != rule:
                self.r['diff']['before'] = rule
                self.r['changed'] = True

        return rules

    def process(self):
        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.p['rule']
            self.p['rule'] = self._add_id_to_rule(rule=self.p['rule'])

            if self.exists:
                if self.r['changed']:
                    self.update()

            else:
                self.create()

        elif self.exists:
            self.delete()

    @staticmethod
    def _split_beg_uid_comment_end(raw: str) -> dict:
        beginning, _r2 = raw.rsplit('comment "', 1)
        uid_comment, end = _r2.split('"', 1)
        split_rule = dict(
            beg=beginning,
            end=end,
            id=None,
        )

        if uid_comment.find(ID_SEPARATOR) != -1:
            uid, cmt = uid_comment.split(ID_SEPARATOR, 1)
            split_rule['id'] = uid
            split_rule['cmt'] = cmt

        else:
            split_rule['cmt'] = uid_comment

        return split_rule

    def _add_id_to_rule(self, rule: str) -> str:
        if rule.find(ID_KEY) == -1:
            if rule.find('comment') == -1:
                comment = ''
                beginning, end = rule, ''

            else:
                split_rule = self._split_beg_uid_comment_end(raw=rule)
                beginning, comment, end = split_rule['beg'], split_rule['cmt'], split_rule['end']

            comment = add_id_to_comment(raw=comment, uid=self.p['id'])
            return f'{beginning}{comment}{end}'

        return rule

    def create(self):
        self.n.cmd_exec(
            cmd=f"add rule {self.p['table']} {self.p['chain']} {self.p['rule']}",
        )

    def delete(self):
        self.n.cmd_exec(
            cmd=f"delete rule {self.p['table']} {self.existing}",
        )

    def update(self):
        self.n.cmd_exec(
            cmd=f"replace rule {self.p['table']} {self.existing} "
                f"{self.p['table']} {self.p['chain']} {self.p['rule']}",
        )
