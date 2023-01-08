from json import loads as json_loads

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.nftables.plugins.module_utils.definition.hc import \
    VALID_ENTRIES
from ansible_collections.ansibleguy.nftables.plugins.module_utils.definition.main import \
    NftTable, NftChain
from ansible_collections.ansibleguy.nftables.plugins.module_utils.definition.rule import \
    NftRule
from ansible_collections.ansibleguy.nftables.plugins.module_utils.definition.sub import \
    NftSet, NftLimit, NftCounter

from ansible_collections.ansibleguy.nftables.plugins.module_utils.check import \
    check_dependencies

check_dependencies()

# pylint: disable=C0413
from nftables import Nftables


# for schema see: https://www.mankier.com/5/libnftables-json


class NFT:
    def __init__(self, module: AnsibleModule):
        self.m = module
        self.n = Nftables()
        self.n.set_json_output(True)
        self.tables = []
        self.chains = []
        self.rules = []
        self.counters = []
        self.limits = []
        self.sets = []

    def _cmd(self, cmd: str) -> list:
        _, stdout, _ = self.n.cmd(cmd)
        data = json_loads(stdout)

        if 'nftables' in data:
            return data['nftables']

        return data

    def get_ruleset(self) -> list:
        return self._cmd(cmd='list ruleset')

    @staticmethod
    def find_item(entries: list, find: str, attr: str = 'name'):
        for item in entries:
            if getattr(item, attr) == find:
                return item

        return None

    def _parse_tables(self, ruleset: list):
        for entry in ruleset:
            if 'table' in entry:
                entry = entry['table']

                self.tables.append(NftTable(raw=entry))

    def _parse_basic(self, ruleset: list, key: str, entries: list, cls):
        for entry in ruleset:
            if key in entry:
                entry = entry[key]
                entries.append(cls(
                    raw=entry,
                    table=self.find_item(
                        entries=self.tables,
                        find=entry['table']
                    ),
                ))

    def _parse_rules(self, ruleset: list):
        for entry in ruleset:
            if 'rule' in entry:
                entry = entry['rule']
                rule = NftRule(
                    table=self.find_item(
                        entries=self.tables,
                        find=entry['table']
                    ),
                    chain=self.find_item(
                        entries=self.chains,
                        find=entry['chain']
                    ),
                    raw=entry,
                )
                rule.init(nft_main=self, raw=entry)
                self.rules.append(self)

    def parse_ruleset(self) -> dict:
        ruleset = self.get_ruleset()

        for entry in ruleset:
            if not any(key in entry for key in VALID_ENTRIES):
                raise SystemExit(f"Got unexpected entry: '{entry}'")

        self._parse_tables(ruleset)

        for key, cls, entries in [
            ('chain', NftChain, self.chains),
            ('counter', NftCounter, self.counters),
            ('limit', NftLimit, self.limits),
            ('set', NftSet, self.sets),
            ('map', NftSet, self.sets),
        ]:
            self._parse_basic(
                ruleset=ruleset,
                cls=cls,
                key=key,
                entries=entries,
            )

        self._parse_rules(ruleset)

        return dict(
            tables=self.tables,
            chains=self.chains,
            rules=self.rules,
            counters=self.counters,
            limits=self.limits,
            sets=self.sets,
        )
