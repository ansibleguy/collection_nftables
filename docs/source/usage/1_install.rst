.. _usage_install:

.. include:: ../_include/head.rst

================
1 - Installation
================


Ansible
*******

See `the documentation <https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#pip-install>`_ on how to install Ansible.

Dependencies
************

Using Shell
===========

First - install nftables!

For the python library to work the installed NFTables version needs to be >= 0.9.3

.. code-block:: bash

    sudo apt install nftables

    # check the installed version
    sudo apt policy nftables

The ansible-modules of this collection use the `python3-nftables module <https://ral-arturo.org/2020/11/22/python-nftables-tutorial.html>`_ to interact with nftables.

You can either install it using your package manager (*apt in the example*) or using pip (*`unofficial version provided by AnsibleGuy <https://github.com/ansibleguy/python3-nftables>`_ *) on the target system.

.. code-block:: bash

    # package manager
    sudo apt install python3-nftables

    # pip => make sure it is installed for the root user or use a virtualenv
    sudo pip install ansibleguy-nftables

Using Ansible
=============

.. code-block:: yaml

    - name: Installing NFTables
      ansible.builtin.package:
        name: ['nftables']  # or ['nftables', 'python3-nftables]

    - name: Installing NFTables python-module
      ansible.builtin.pip:
        name: 'ansibleguy-nftables'

    - name: Enabling and starting NFTables
      ansible.builtin.service:
        name: 'nftables.service'
        state: started
        enabled: true


Collection
**********

.. code-block:: bash

    # unstable/latest version:
    ansible-galaxy collection install git+https://github.com/ansibleguy/collection_nftables.git

    # install to specific director for easier development
    cd $PLAYBOOK_DIR
    ansible-galaxy collection install git+https://github.com/ansibleguy/collection_nftables.git -p ./collections
