# Contributing

* report errors as [issues](https://github.com/ansibleguy/collection_nftables/issues)
* test unstable modules and [report if they work as expected](https://github.com/ansibleguy/collection_nftables/discussions/new?category=general)
* add [ansible-based tests](https://github.com/ansibleguy/collection_nftables/blob/latest/tests) for some error-case(s) you have encountered
* extend or correct the [documentation](https://github.com/ansibleguy/collection_nftables/blob/latest/docs)
* add missing inline documentation [as standardized](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html#documentation-block)
  * should be placed in `<COLLECTION>/plugins/module_utils/inline_docs/<MODULE>.py` and then imported in the module
* contribute code fixes or optimizations
* implement additional modules

## Module changes

Whenever you change a module's code - you should run lint (`bash scripts/lint.sh`) and [its tests](https://github.com/ansibleguy/collection_nftables/blob/latest/tests/README.md)!

TLDR:
* Set up a VM or Container
* Run the Module: `bash scripts/test.sh -e test_module=<MODULE>`
