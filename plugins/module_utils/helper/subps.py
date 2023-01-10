import subprocess

from ansible_collections.ansibleguy.nftables.plugins.module_utils.helper.main import is_in


def _format_command(cmd: (str, list)) -> list:
    if not isinstance(cmd, (str, list)):
        raise ValueError(f"Command needs to be either string or list - got: {type(cmd)}")

    if isinstance(cmd, list):
        return cmd

    if is_in(' ', cmd):
        return cmd.split(' ')

    return [cmd]


def process(cmd: (str, list), timeout_sec: int = None) -> dict:
    try:
        with subprocess.Popen(
            _format_command(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ) as p:
            b_stdout, b_stderr = p.communicate(timeout=timeout_sec)
            stdout, stderr, rc = b_stdout.decode('utf-8').strip(), b_stderr.decode('utf-8').strip(), p.returncode

    except (subprocess.TimeoutExpired, subprocess.SubprocessError, subprocess.CalledProcessError,
            OSError, IOError) as error:
        stdout, stderr, rc = None, str(error), 1

    return dict(
        stdout=stdout,
        stderr=stderr,
        rc=rc,
    )
