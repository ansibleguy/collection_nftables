from ansible.module_utils.basic import AnsibleModule


class BaseModule:
    def __init__(self, module: AnsibleModule, result: dict):
        self.m = module
        self.r = result
        self.p = module.params

    def check(self) -> None:
        # check if changed & pre-processing
        pass

    def process(self) -> None:
        # make changes
        pass

    def get(self) -> list:
        # pull existing entries
        pass
