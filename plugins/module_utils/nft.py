from json import loads as json_loads

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.nftables.plugins.module_utils.check import \
    check_dependencies

check_dependencies()

# pylint: disable=C0413
from nftables import Nftables

RULE_ACTIONS = ['accept', 'drop', 'reject', 'jump', 'return']
VALID_ENTRIES = ['metainfo', 'table', 'chain', 'rule']


class NftItem:
    def __init__(self, handle: int):
        self.handle = handle


class NftTable(NftItem):
    def __init__(self, family: str, name: str, handle: int):
        NftItem.__init__(self=self, handle=handle)
        self.family = family
        self.name = name


class NftChain(NftItem):
    def __init__(self, family: str, name: str, handle: int, table: NftTable):
        NftItem.__init__(self=self, handle=handle)
        self.table = table
        self.family = family
        self.name = name


class NftRuleMatch:
    def __init__(self, operator: str, key: str, value: str):
        self.operator = operator
        self.key = key
        self.value = value


class NftRuleCounter:
    def __init__(self, operator: str, key: str, value: str):
        self.operator = operator
        self.key = key
        self.value = value


class NftRuleJump:
    def __init__(self, chain: NftChain):
        self.chain = chain


class NftRule(NftItem):
    def __init__(
            self, family: str, handle: int, matches: list, action: str,
            table: NftTable, chain: NftChain, raw: dict, jump: (NftRuleJump, None)
    ):
        NftItem.__init__(self=self, handle=handle)
        self.table = table
        self.chain = chain
        self.family = family
        self.raw = raw
        self.matches = matches
        self.jump = jump
        self.action = action


class NFT:
    def __init__(self, module: AnsibleModule):
        self.m = module
        self.n = Nftables()
        self.n.set_json_output(True)
        self.tables = []
        self.chains = []
        self.rules = []

    def _cmd(self, cmd: str) -> list:
        _, stdout, _ = self.n.cmd(cmd)
        data = json_loads(stdout)

        if 'nftables' in data:
            return data['nftables']

        return data

    def get_ruleset(self) -> list:
        return self._cmd(cmd='list ruleset')

    def _find_table(self, name: str) -> (NftTable, None):
        for table in self.tables:
            if table.name == name:
                return table

        return None

    def _find_chain(self, name: str) -> (NftChain, None):
        for chain in self.chains:
            if chain.name == name:
                return chain

        return None

    @staticmethod
    def _parse_rule_match(expression: dict, side: str) -> str:
        parts = []
        side = expression['match'][side]

        if isinstance(side, dict):
            for v in side.values():
                if isinstance(v, dict):
                    for v2 in v.values():
                        parts.append(v2)

                else:
                    parts.append(v)

        else:
            parts.append(side)

        return ' '.join(map(str, parts))

    def parse_ruleset(self):
        ruleset = self.get_ruleset()
        for entry in ruleset:
            if not any(key in entry for key in VALID_ENTRIES):
                raise SystemExit(f"Got unexpected entry: '{entry}'")

        for entry in ruleset:
            if 'table' in entry:
                entry = entry['table']

                self.tables.append(
                    NftTable(
                        family=entry['family'],
                        name=entry['name'],
                        handle=entry['handle'],
                    )
                )

        for entry in ruleset:
            if 'chain' in entry:
                entry = entry['chain']

                self.chains.append(
                    NftChain(
                        family=entry['family'],
                        name=entry['name'],
                        handle=entry['handle'],
                        table=self._find_table(name=entry['table'])
                    )
                )

        for entry in ruleset:
            if 'rule' in entry:
                entry = entry['rule']

                matches = []
                jump = None
                action = None

                for expression in entry['expr']:
                    # expr: 'xt', 'limit', 'counter', 'match'
                    #   'accept', 'jump', 'drop', 'return',
                    for a in RULE_ACTIONS:
                        if a in expression:
                            action = a

                    if 'match' in expression:
                        matches.append(
                            NftRuleMatch(
                                operator=expression['match']['op'],
                                key=self._parse_rule_match(expression=expression, side='left'),
                                value=self._parse_rule_match(expression=expression, side='right'),
                            )
                        )

                    if 'jump' in expression:
                        jump = NftRuleJump(chain=self._find_chain(expression['jump']['target']))

                self.rules.append(
                    NftRule(
                        family=entry['family'],
                        handle=entry['handle'],
                        table=self._find_table(entry['table']),
                        chain=self._find_chain(entry['chain']),
                        raw=entry,
                        action=action,
                        jump=jump,
                        matches=matches,
                    )
                )
