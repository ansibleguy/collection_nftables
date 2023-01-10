from ansible_collections.ansibleguy.nftables.plugins.module_utils.definition.hc import \
    ID_SEPARATOR, ID_KEY


def get_uid_comment(uid: str) -> str:
    return f'{ID_KEY}{uid}{ID_SEPARATOR}'


def clean_comment(comment: str) -> str:
    replacement = {
        '_': [ID_SEPARATOR * 2, ID_SEPARATOR],
        '': ['comment ""', 'comment " "'],
    }

    for new, old_list in replacement.items():
        for old in old_list:
            comment.replace(old, new)

    return comment
