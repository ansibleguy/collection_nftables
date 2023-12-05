import pytest


@pytest.mark.parametrize('raw_version, result', [
    ('invalid', False),  # non-version number
    ('v0.8.3', False),  # to low version
    ('v0.9.4', True),  # basic version
    ('nftables v1.0.6 (Lester Gooch #5)', True),  # extended version
])
def test_version_check(raw_version: str, result: bool):
    # pylint: disable=C0415
    from ansible_collections.ansibleguy.nftables.plugins.module_utils.check import _validate_version
    assert _validate_version(raw_version) is result
