from ansible_collections.ansibleguy.nftables.plugins.module_utils.helper.main import \
    value_or_none

# for schema see: https://www.mankier.com/5/libnftables-json


class NftItem:
    def __init__(self, raw: dict, table=None):
        self.handle = raw['handle']
        if table is not None:
            self.table = table

        if hasattr(self, 'RAW_ITEMS'):
            for key in self.RAW_ITEMS:
                setattr(self, key, value_or_none(raw, key))

    def __repr__(self):
        # pylint: disable=E1101
        info = ', '.join([f'{key.upper()} {getattr(self, key)}' for key in self.RAW_ITEMS])
        table = f", Table '{self.table.name}'" if hasattr(self, 'table') else ''
        return f"{self.KEY} {info}{table} | ID {self.handle}"


class NftTable(NftItem):
    KEY = 'Table'
    RAW_ITEMS = ['family', 'name']

    def __init__(self, raw: dict):
        NftItem.__init__(self=self, raw=raw)


class NftChain(NftItem):
    KEY = 'Chain'
    RAW_ITEMS = ['family', 'name', 'type', 'hook', 'prio', 'dev', 'policy']

    def __init__(self, raw: dict, table: NftTable):
        NftItem.__init__(self=self, raw=raw, table=table)
