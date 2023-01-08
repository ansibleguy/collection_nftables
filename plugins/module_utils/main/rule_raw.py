from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.nftables.plugins.module_utils.base import BaseModule


class RuleRaw(BaseModule):
    def __init__(self, module: AnsibleModule, result: dict):
        BaseModule.__init__(self=self, module=module, result=result)
