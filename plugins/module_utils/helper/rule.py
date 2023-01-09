from ansible_collections.ansibleguy.nftables.plugins.module_utils.definition.hc import \
    ID_SEPARATOR, ID_KEY


def get_uid_comment(uid: str) -> str:
    return f'{ID_KEY}{uid}{ID_SEPARATOR}'


def clean_comment(comment: str) -> str:
    return comment.replace(ID_SEPARATOR * 2, '_').replace(ID_SEPARATOR, '_')
