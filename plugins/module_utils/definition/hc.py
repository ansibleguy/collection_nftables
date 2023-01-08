RULE_ACTIONS = ['accept', 'drop', 'continue', 'jump', 'return', 'goto']
MAIN_ENTRIES = ['table', 'chain', 'rule', 'counter', 'limit', 'set']
SUB_ENTRIES = ['metainfo', 'map', 'element', 'flowtable', 'quota', 'ct helper', 'ct timeout', 'ct expectation']
VALID_ENTRIES = MAIN_ENTRIES.copy()
VALID_ENTRIES.extend(SUB_ENTRIES)
ID_KEY = 'ID='
ID_SEPARATOR = '|'
