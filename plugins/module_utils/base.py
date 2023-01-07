from ansible.module_utils.basic import AnsibleModule


class BaseModule:
    def __init__(self, module: AnsibleModule, result: dict):
        self.m = module
        self.r = result
        self.p = module.params

    def check(self) -> None:
        pass

    def process(self) -> None:
        pass

    def reload(self) -> None:
        pass

    def list(self) -> list:
        return []
