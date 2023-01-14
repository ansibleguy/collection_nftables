from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.nftables.plugins.module_utils.nft import NFT


class BaseModule:
    def __init__(self, module: AnsibleModule, result: dict):
        self.m = module
        self.r = result
        self.p = module.params
        self.exists = False
        self.existing = None
        self.n = NFT(module=module, result=result)

    def check(self) -> None:
        # check if changed & pre-processing
        pass

    def process(self) -> None:
        # make changes
        pass

    def get(self) -> list:
        # pull existing entries
        pass
