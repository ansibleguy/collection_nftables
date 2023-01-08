from ansible_collections.ansibleguy.nftables.plugins.module_utils.definition.hc import \
    ID_SEPARATOR, ID_KEY


def add_id_to_comment(raw: str, uid: str) -> str:
    return f'"{ID_KEY}{uid}{ID_SEPARATOR}{raw}"'
