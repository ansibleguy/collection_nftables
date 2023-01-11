from json import loads as json_loads

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.nftables.plugins.module_utils.definition.hc import \
    VALID_ENTRIES
from ansible_collections.ansibleguy.nftables.plugins.module_utils.helper.main import is_in
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
    HANDLE_SEPARATOR = ' # handle '
    CHECK_MODE_CMDS = ['list ruleset']

    def __init__(self, module: AnsibleModule, result: dict):
        self.m = module
        self.r = result
        self.n = Nftables()
        self.tables = []
        self.chains = []
        self.rules = []
        self.counters = []
        self.limits = []
        self.sets = []

    def _cmd_prep(self, cmd) -> bool:
        self.r['_executed'].append(cmd)
        return not self.m.check_mode or cmd in self.CHECK_MODE_CMDS

    def _cmd_raw(self, cmd: str) -> list:
        if self._cmd_prep(cmd):
            self.n.set_json_output(False)
            self.n.set_handle_output(True)
            _, stdout, _ = self.n.cmd(cmd)
            return stdout.replace('\t', '').split('\n')

        return []

    def _cmd_json(self, cmd: str) -> list:
        if self._cmd_prep(cmd):
            self.n.set_json_output(True)
            _, stdout, _ = self.n.cmd(cmd)

            data = json_loads(stdout)

            if 'nftables' in data:
                return data['nftables']

            return data

        return []

    def cmd_exec(self, cmd: str):
        if self._cmd_prep(cmd):
            self.n.set_json_output(False)
            self.n.set_handle_output(False)
            rc, stdout, stderr = self.n.cmd(cmd.strip().replace('\n', ''))

            if rc != 0:
                self.r['_fail_info']['rc'] = rc
                self.r['_fail_info']['stdout'] = stdout
                self.r['_fail_info']['stderr'] = stderr
                self.m.fail_json(msg=f"Command '{cmd}' FAILED with error: '{stderr}'", **self.r)

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

    def ruleset_raw(self) -> dict:
        # returns ruleset as shown in the config file
        stdout_lines = self._cmd_raw('list ruleset')
        data, table, chain = {}, None, None

        for line in stdout_lines:
            entry = line.strip()
            if entry in ['', '}']:
                continue

            if entry.startswith('table'):
                table = entry.split(' ', 1)[1].rsplit(' ', 4)[0]
                data[table] = {}

            elif entry.startswith('chain'):
                chain = entry.split(' ', 2)[1]
                data[table][chain] = []

            elif table is None or chain is None:
                # should not happen
                raise SystemExit(f"Got unexpected entry: '{entry}'")

            else:
                handle = None
                if is_in(self.HANDLE_SEPARATOR, entry):
                    entry, handle = entry.split(self.HANDLE_SEPARATOR)

                data[table][chain].append({'rule': entry, 'handle': handle})

        return data

    def parse_ruleset(self) -> dict:
        # returns objectified ruleset
        ruleset = self._cmd_json(cmd='list ruleset')

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
