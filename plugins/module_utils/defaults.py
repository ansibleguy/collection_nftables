from packaging import version

CONFIG = dict(
    path_log='/tmp/ansibleguy.nftables',
    min_version=version.parse('0.9.3'),
)

NFT_MOD_ARGS = dict(
    debug=dict(type='bool', required=False, default=False),
)
