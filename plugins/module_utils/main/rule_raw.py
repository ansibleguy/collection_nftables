from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.nftables.plugins.module_utils.base import BaseModule

from ansible_collections.ansibleguy.nftables.plugins.module_utils.nft import NFT
from ansible_collections.ansibleguy.nftables.plugins.module_utils.helper.rule import \
    get_uid_comment, clean_comment
from ansible_collections.ansibleguy.nftables.plugins.module_utils.definition.hc import \
    ID_SEPARATOR, ID_KEY


class RuleRaw(BaseModule):
    def __init__(self, module: AnsibleModule, result: dict):
        BaseModule.__init__(self=self, module=module, result=result)
        self.exists = False
        self.existing = None
        self.n = NFT(module=module, result=result)

    def check(self):
        if self.p['state'] == 'present':
            if self.p['rule'] is None:
                self.m.fail_json(
                    "You need to supply a value for the 'rule' parameter "
                    'to create one!'
                )

            self.r['diff']['after'] = clean_comment(self.p['rule'])

        rules = self._build_rules(
            self._get_table()
        )

        if self.p['id'] in rules:
            self.exists = True
            self.existing = rules[self.p['id']]['handle']
            rule_item = rules[self.p['id']]

            if self.p['state'] == 'present':
                # update
                self.r['diff']['before'] = rule_item['rule']

                if self.r['diff']['before'] != self.r['diff']['after']:
                    self.r['changed'] = True

            else:
                # delete
                self.r['changed'] = True

        else:
            self.r['test'] = f"{self.p['id']} not in {rules}"
            # create
            if self.p['state'] == 'present':
                self.r['changed'] = True

        return rules

    def _build_rules(self, table: dict) -> dict:
        rules = {}

        for entry in table[self.p['chain']]:
            for rule, handle in entry.items():
                if handle is None:
                    continue

                if rule.find(ID_KEY) != -1 and rule.find(ID_SEPARATOR) != -1 and rule.find('comment') != -1:
                    # only try to match rules managed by the modules
                    split_rule = self._split_beg_uid_comment_end(raw=rule)
                    rule_new = f"{split_rule['beg']}{split_rule['end']}"
                    rules[split_rule['id']] = {'rule': rule_new, 'handle': handle}

        return rules

    def _get_table(self) -> dict:
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

        return table

    def process(self):
        if self.p['state'] == 'present':
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
        # extract comment from rule to add its rule-id in its beginning
        if raw.find('comment') == -1:
            return dict(beg=f'{raw}"', id=None, end='"')

        if raw.find(ID_KEY) != -1:
            # extract id if present
            beg, uid_cmt_end = raw.rsplit(ID_KEY, 1)
            uid, cmt_end = uid_cmt_end.split(ID_SEPARATOR, 1)
            cmt_end = clean_comment(cmt_end)
            return dict(beg=beg, id=uid, end=cmt_end)

        # make place for id if comment is present
        beg, cmt_end = raw.split('comment "', 1)
        return dict(beg=f'{beg}comment "', id=None, end=cmt_end)

    def _add_id_to_rule(self, rule: str) -> str:
        if rule.find(ID_KEY) == -1:
            if rule.find('comment') == -1:
                beg, end = f'{rule} comment "', '"'

            else:
                split_rule = self._split_beg_uid_comment_end(raw=rule)
                beg, end = split_rule['beg'], split_rule['end']

            return f"{beg}{get_uid_comment(uid=self.p['id'])}{end}"

        return rule

    def create(self):
        self.n.cmd_exec(
            cmd=f"add rule {self.p['table']} {self.p['chain']} {self.p['rule']}",
        )

    def delete(self):
        self.n.cmd_exec(
            cmd=f"delete rule {self.p['table']} {self.p['chain']} handle {self.existing}",
        )

    def update(self):
        self.n.cmd_exec(
            cmd=f"replace rule {self.p['table']} {self.p['chain']} handle {self.existing} "
                f"{self.p['rule']}",
        )
