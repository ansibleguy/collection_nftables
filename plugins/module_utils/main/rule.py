from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.nftables.plugins.module_utils.base import BaseModule


class Rule(BaseModule):
    def __init__(self, module: AnsibleModule, result: dict):
        BaseModule.__init__(self=self, module=module, result=result)
