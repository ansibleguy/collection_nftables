from ansible_collections.ansibleguy.nftables.plugins.module_utils.helper.main import \
    value_or_none

from ansible_collections.ansibleguy.nftables.plugins.module_utils.definition.hc import \
    RULE_ACTIONS, ID_SEPARATOR, ID_KEY
from ansible_collections.ansibleguy.nftables.plugins.module_utils.helper.main import is_in
from ansible_collections.ansibleguy.nftables.plugins.module_utils.definition.main import \
    NftTable, NftItem, NftChain
from ansible_collections.ansibleguy.nftables.plugins.module_utils.definition.sub import \
    NftMatch, NftJump, NftLimit, NftGoTo

# for schema see: https://www.mankier.com/5/libnftables-json


class NftRule(NftItem):
    KEY = 'Rule'
    RAW_ITEMS = ['comment', 'index']
    DATA_ITEMS = ['family', 'matches', 'jump', 'goto', 'action', 'counter', 'limit']

    def __init__(self, table: NftTable, chain: NftChain, raw: dict):
        NftItem.__init__(self=self, raw=raw, table=table)
        self.chain = chain
        self.id = None

    def init(self, nft_main, raw: dict):
        data = dict(
            matches=[],
            jump=None,
            goto=None,
            action=None,
            comment=None,
            counter=False,
            limit=None,
        )

        for expression in raw['expr']:
            for a in RULE_ACTIONS:
                if a in expression:
                    data['action'] = a

            self._init_match(d=data, e=expression)
            self._init_comment(d=data, e=expression)
            self._init_counter(d=data, e=expression, n=nft_main)
            self._init_limit(d=data, e=expression, n=nft_main)
            self._init_jump(d=data, e=expression, n=nft_main)
            self._init_goto(d=data, e=expression, n=nft_main)

        for key in self.DATA_ITEMS:
            setattr(self, key, value_or_none(data, key))

    @staticmethod
    def _init_goto(e: dict, d: dict, n):
        if 'goto' in e:
            d['goto'] = NftGoTo(
                chain=n.find_item(
                    entries=n.chains,
                    find=e['goto']['target'],
                )
            )

    @staticmethod
    def _init_jump(e: dict, d: dict, n):
        if 'jump' in e:
            d['jump'] = NftJump(
                chain=n.find_item(
                    entries=n.chains,
                    find=e['jump']['target'],
                )
            )

    def _init_comment(self, e: dict, d: dict):
        if 'comment' in e:
            d['comment'] = self._id_from_comment(e['comment'])

    def _init_match(self, e: dict, d: dict):
        if 'match' in e:
            d['matches'].append(
                NftMatch(
                    operator=e['match']['op'],
                    left=self._parse_rule_match(
                        expression=e, side='left'
                    ),
                    right=self._parse_rule_match(
                        expression=e, side='right'
                    ),
                )
            )

    @staticmethod
    def _init_counter(e: dict, d: dict, n):
        if 'counter' in e:
            if 'packets' in e['counter']:
                d['counter'] = True

            else:
                d['counter'] = n.find_item(
                    entries=n.counters,
                    find=e['counter'],
                )

    def _init_limit(self, e: dict, d: dict, n):
        if 'limit' in e:
            if 'rate' in e['limit']:
                d['limit'] = NftLimit(
                    raw=e['limit'],
                    table=self.table
                )

            else:
                n.find_item(
                    entries=n.limits,
                    find=e['limit'],
                )

    def _id_from_comment(self, cmt: str) -> str:
        if cmt.startswith(ID_KEY) and is_in(ID_SEPARATOR, cmt):
            self.id, cmt = cmt.replace(ID_KEY, '').split(ID_SEPARATOR, 1)
            if self.id.startswith('"'):
                self.id = self.id[1:]

            if self.id.endswith('"'):
                self.id = self.id[:-1]

        return cmt

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

    def __repr__(self):
        info = ', '.join([f'{key.upper()} {getattr(self, key)}' for key in self.DATA_ITEMS])
        info2 = ', '.join([f'{key.upper()} {getattr(self, key)}' for key in self.RAW_ITEMS])
        return f"{self.KEY} {info}, {info2} | ID {self.handle}"
