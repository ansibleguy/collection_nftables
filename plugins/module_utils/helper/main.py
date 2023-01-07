from typing import Callable
from ipaddress import ip_address, ip_network

from ansible.module_utils.basic import AnsibleModule


def diff_remove_empty(diff: dict) -> dict:
    d = diff.copy()
    for k in diff.keys():
        if len(diff[k]) == 0:
            d.pop(k)

    return d


def ensure_list(data: (int, str, list, None)) -> list:
    # if user supplied a string instead of a list => convert it to match our expectations
    if isinstance(data, list):
        return data

    if data is None:
        return []

    return [data]


def is_ip(host: str, ignore_empty: bool = False) -> bool:
    if ignore_empty and host in ['', ' ']:
        return True

    valid_ip = False

    try:
        ip_address(host)
        valid_ip = True

    except ValueError:
        pass

    return valid_ip


def is_ip_or_network(entry: str, strict: bool = False) -> bool:
    valid = is_ip(entry)

    if not valid:
        try:
            ip_network(entry, strict=strict)
            valid = True

        except ValueError:
            valid = False

    return valid


def validate_port(module: AnsibleModule, port: (int, str), error_func: Callable = None) -> bool:
    if error_func is None:
        error_func = module.fail_json

    if port in ['any', '']:
        return True

    try:
        if int(port) < 1 or int(port) > 65535:
            error_func(f"Value '{port}' is an invalid port!")
            return False

    except (ValueError, TypeError):
        error_func(f"Value '{port}' is an invalid port!")
        return False

    return True


def sort_param_lists(params: dict) -> None:
    for k in params:
        if isinstance(params[k], list):
            params[k].sort()
