from ansible_collections.ansibleguy.nftables.plugins.module_utils.definition.main import \
    NftTable, NftItem, NftChain

# for schema see: https://www.mankier.com/5/libnftables-json


# common items

class NftMatch:
    KEY = 'Match'

    def __init__(self, operator: str, left: str, right: str):
        self.operator = operator
        self.left = left
        self.right = right


class NftCounter(NftItem):
    KEY = 'Counter'
    RAW_ITEMS = ['family', 'name', 'packets', 'bytes']

    def __init__(self, raw: dict, table: NftTable):
        NftItem.__init__(self=self, raw=raw, table=table)


class NftLimit(NftItem):
    KEY = 'Limit'
    RAW_ITEMS = ['family', 'name', 'rate', 'per', 'burst', 'unit', 'inv']

    def __init__(self, raw: dict, table: NftTable):
        NftItem.__init__(self=self, raw=raw, table=table)


class NftSet(NftItem):
    KEY = 'Set'
    RAW_ITEMS = [
        'name', 'family', 'type', 'policy', 'flags', 'elem', 'timeout',
        'gc-interval', 'size'
    ]

    def __init__(self, raw: dict, table: NftTable):
        NftItem.__init__(self=self, raw=raw, table=table)

    def __repr__(self) -> str:
        info = ', '.join([f'{key.upper()} {getattr(self, key)}' for key in self.RAW_ITEMS])
        return f"Set {info}, Table '{self.table.name}' | ID {self.handle}"


class NftJump:
    def __init__(self, chain: NftChain):
        self.chain = chain

    def __repr__(self) -> str:
        return f"Jump to chain{self.chain.name}"


class NftGoTo:
    def __init__(self, chain: NftChain):
        self.chain = chain

    def __repr__(self) -> str:
        return f"Go to chain{self.chain.name}"


# for special-cases

class NftQuota(NftItem):
    KEY = 'Quota'
    RAW_ITEMS = ['family', 'name', 'bytes', 'used', 'inv']

    def __init__(self, raw: dict, table: NftTable):
        NftItem.__init__(self=self, raw=raw, table=table)


class NftFlowtable(NftItem):
    KEY = 'Flowtable'
    RAW_ITEMS = ['family', 'name', 'hook', 'prio', 'dev']

    def __init__(self, raw: dict, table: NftTable):
        NftItem.__init__(self=self, raw=raw, table=table)


class NftElement(NftItem):
    KEY = 'Element'
    RAW_ITEMS = ['family', 'name', 'elem']

    def __init__(self, raw: dict, table: NftTable):
        NftItem.__init__(self=self, raw=raw, table=table)


class NftCtHelper(NftItem):
    KEY = 'CT-Helper'
    RAW_ITEMS = ['family', 'name', 'type', 'protocol', 'l3proto']

    def __init__(self, raw: dict, table: NftTable):
        NftItem.__init__(self=self, raw=raw, table=table)


class NftCtExpectation(NftItem):
    KEY = 'CT-Expectation'
    RAW_ITEMS = ['family', 'name', 'l3proto', 'protocol', 'dport', 'timeout', 'size']

    def __init__(self, raw: dict, table: NftTable):
        NftItem.__init__(self=self, raw=raw, table=table)


class NftCtTimeout(NftItem):
    KEY = 'CT-Timeout'
    RAW_ITEMS = ['family', 'name', 'protocol', 'state', 'value', 'l3proto']

    def __init__(self, raw: dict, table: NftTable):
        NftItem.__init__(self=self, raw=raw, table=table)
