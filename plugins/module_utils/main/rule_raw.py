from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.nftables.plugins.module_utils.base import BaseModule

from ansible_collections.ansibleguy.nftables.plugins.module_utils.nft import NFT
from ansible_collections.ansibleguy.nftables.plugins.module_utils.helper.main import is_in
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
        self.position = None  # position the rule should be placed in (before/after)
        self.before_after_handle = None

    def check(self):
        if self.p['state'] == 'present':
            if self.p['rule'] is None:
                self.m.fail_json(
                    "You need to supply a value for the 'rule' parameter "
                    'to create one!'
                )

            self.r['diff']['after'] = clean_comment(self.p['rule']).strip()

        rules = self._build_rules(self._get_table())

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
            # create
            if self.p['state'] == 'present':
                self.r['changed'] = True

        self._find_before_after(key='before', rules=rules)
        self._find_before_after(key='after', rules=rules)

        if not self.r['changed']:
            self.r['changed'] = self._position_changed(rules)

        return rules

    def _position_changed(self, rules: dict) -> bool:
        if self.p['id'] not in rules:
            return False

        position = rules[self.p['id']]['line']
        other, other_position = None, -1
        check, check_position = None, None

        if self.p['before'] is not None:
            other = self.p['before']
            check = 'b'

        if self.p['after'] is not None:
            other = self.p['after']
            check = 'a'

        if other is None:
            return False

        for uid, values in rules.items():
            if uid == other:
                other_position = values['line']

        if other is None:
            self.m.warn(f"Provided rule was not found: '{other}'")
            return False

        if check == 'b':
            check_position = other_position - 1

        else:
            check_position = other_position + 1

        return position != check_position

    def _find_before_after(self, key: str, rules: dict):
        if self.p[key] is not None:
            if self.p[key] in rules:
                self.before_after_handle = rules[self.p[key]]['handle']

    def _build_rules(self, table: dict) -> dict:
        rules = {}
        entry_line = 1

        for entry in table[self.p['chain']]:
            if entry['handle'] is None:
                continue

            if all([
                is_in(ID_KEY, entry['rule']),
                is_in(ID_SEPARATOR, entry['rule']),
                is_in('comment', entry['rule'])
            ]):
                # only try to match rules managed by the modules
                split_rule = self._split_beg_uid_comment_end(raw=entry['rule'])
                rule_new = f"{split_rule['beg']}{split_rule['end']}".strip()
                rules[split_rule['id']] = {
                    'rule': rule_new,
                    'handle': entry['handle'],
                    'line': entry_line
                }

            entry_line += 1

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

        self.r['chain'] = table[self.p['chain']]
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

    def _split_beg_uid_comment_end(self, raw: str) -> dict:
        # extract comment from rule to add its rule-id in its beginning
        if not is_in('comment', raw):
            return dict(beg=f'{raw}"', id=None, end='"')

        if is_in(ID_KEY, raw):
            empty_cmt = is_in(
                f"comment \"{get_uid_comment(uid=self.p['id'])}\"",
                raw,
            )

            # extract id if present
            beg, uid_cmt_end = raw.rsplit(ID_KEY, 1)
            uid, cmt_end = uid_cmt_end.split(ID_SEPARATOR, 1)
            cmt_end = clean_comment(cmt_end)

            # remove empty comment (only added for ID)
            if empty_cmt:
                beg = beg.replace('comment "', '')
                cmt_end = cmt_end[1:]

            return dict(beg=beg, id=uid, end=cmt_end)

        # make place for id if comment is present
        beg, cmt_end = raw.split('comment "', 1)
        return dict(beg=f'{beg}comment "', id=None, end=cmt_end)

    def _add_id_to_rule(self, rule: str) -> str:
        if is_in(ID_KEY, rule):
            return rule

        if not is_in('comment', rule):
            beg, end = f'{rule} comment "', '"'

        else:
            split_rule = self._split_beg_uid_comment_end(raw=rule)
            beg, end = split_rule['beg'], split_rule['end']

        return f"{beg}{get_uid_comment(uid=self.p['id'])}{end}"

    def create(self):
        position = ''
        action = 'add'

        if self.before_after_handle is not None:
            position = f" position {self.before_after_handle}"

        if self.p['before'] is not None:
            action = 'insert'

        self.n.cmd_exec(
            cmd=f"{action} rule {self.p['table']} {self.p['chain']}{position} {self.p['rule']}",
        )

    def delete(self):
        self.n.cmd_exec(
            cmd=f"delete rule {self.p['table']} {self.p['chain']} handle {self.existing}",
        )

    def update(self):
        if self.before_after_handle is not None:
            # could not find option to set position when calling 'replace'
            self.create()
            self.delete()

        else:
            self.n.cmd_exec(
                cmd=f"replace rule {self.p['table']} {self.p['chain']} handle {self.existing} "
                    f"{self.p['rule']}",
            )
