from pathlib import Path
from os import environ
from packaging import version

from ansible_collections.ansibleguy.nftables.plugins.module_utils.defaults import CONFIG
from ansible_collections.ansibleguy.nftables.plugins.module_utils.helper.subps import \
    process


def _check_nft_version() -> bool:
    nft_version = version.parse('0')  # will also fail if nft is not installed

    for search_dir in environ['PATH'].split(':'):
        if Path(f"{search_dir}/nft").exists():
            result = process(cmd=['nft', '--version'])

            for part in result['stdout'].split(' '):
                try:
                    _v = version.parse(part)
                except version.InvalidVersion:
                    # version.parse throw exceptions if part is not parsable as a version
                    _v = None 
                if isinstance(_v, version.Version):
                    nft_version = _v
                    break

    return nft_version >= CONFIG['min_version']


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
