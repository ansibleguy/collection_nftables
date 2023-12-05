import pytest


@pytest.mark.parametrize('cmd, rc, stdout', [
    ('which mkdir', 0, '/usr/bin/mkdir'),
    ('some-invalid-command', 1, None),  # soft cmd failure
])
def test_process(cmd: str, rc: int, stdout: str):
    # pylint: disable=C0415
    from ansible_collections.ansibleguy.nftables.plugins.module_utils.helper.subps import process
    result = process(cmd)

    assert result['rc'] == rc

    if stdout is not None:
        assert result['stdout'].strip() == stdout
