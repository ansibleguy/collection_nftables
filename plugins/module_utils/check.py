from re import match as regex_match
from packaging import version

from ansible_collections.ansibleguy.nftables.plugins.module_utils.defaults import CONFIG
from ansible_collections.ansibleguy.nftables.plugins.module_utils.helper.subps import \
    process


def _check_nft_version() -> bool:
    result = process(cmd=['nft', '--version'])
    if result['rc'] != 0:
        return False

    return _validate_version(result['stdout'])


def _validate_version(raw_version: str) -> bool:
    # regex for semantic versioning
    vers = regex_match(r'.*(v[0-9\\.]*?)(\s|$)', raw_version)
    if vers:
        try:
            vers = version.parse(vers[1])
            if isinstance(vers, version.Version):
                return vers >= CONFIG['min_version']

        except IndexError:
            pass

    return False

def check_dependencies() -> None:
    try:
        # pylint: disable=C0415
        from nftables import Nftables

        rc, _, _ = Nftables().cmd('list ruleset')
        if rc == -1:
            raise SystemExit(
                'You need to run this module as root '
                'so it can interact with NFTables!'
            )

    except (ModuleNotFoundError, ImportError):
        # pylint: disable=W0707
        raise SystemExit(
            'For this Ansible-module to work you must install its dependencies first: '
            "'sudo apt install nftables python3-nftables'"
        )

    if not _check_nft_version():
        raise SystemExit(
            f"NFTables version >= {CONFIG['min_version']} needs to be installed to "
            'use this module!'
        )
