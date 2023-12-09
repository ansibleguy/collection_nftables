# ansibleguy.nftables - Testing

As NFTables behaves differently in containers, we are testing on a Linux VM and a Linux Container (_LXC > Docker_).

Both must be reachable by SSH as **we are using Ansible directly for integration-testing**.

----

## Setup

You can also only set-up one of these test-systems.

But you will have to run Ansible by using the `--limit=container` or `--limit=vm` argument.

Python libraries: `apt install python3-nftables python3-packaging`

### Virtual Machine

We are using a [Debian 12 minimal]() installation.

For a quick-start you could use [this VirtualBox image](https://sourceforge.net/projects/linuxvmimages/) provided by [linuxvmimages.com](https://www.linuxvmimages.com/images/debian-12/).

### Container

We are using a Debian 12 container.

I would recommend using [a LXC](https://wiki.debian.org/LXC) if you have the needed system for it.

* [Proxmox LXC](https://pve.proxmox.com/wiki/Linux_Container#pct_container_images):

   ```bash
   pveam update
   pveam download local debian-12-standard_12.2-1_amd64.tar.zst  # exact version number could vary
   ```

* [Raw LXC](https://wiki.debian.org/LXC#Container_Creation)

* Docker: `docker pull debian:12`

   You will have to install NFTables and make sure to use the ssh-server as entrypoint:

   ```
   EXPOSE 1222
   CMD ["/usr/sbin/sshd","-D", "-p", "1222", "-o", "ListenAddress=0.0.0.0"]
   ```

### Config

Add your test-system's IPs and users to the `inventory/host_vars/*.yml` files OR use the environmental variables:

```bash
export TEST_VM=192.168.0.1
export TEST_CONT=192.168.0.2
export TEST_PORT=1222
export TEST_USER=dummy
export TEST_PWD=test123
```

A NFTables base-config might be added later on.

----

## Add/Modify

When modifying tests you should run the lint-script: `bash scripts/lint.sh`

Tests are placed under: `tests/tasks/` and should be named as the module they are testing.

Example: `tests/tasks/list.yml` is testing `ansibleguy.nftables.list`

Tests should always clean up after itself so the test-system is back to the state it was in before! Add those cleanup-tasks in `tests/tasks/<MODULE>_cleanup.yml`

As the connection over SSH is needed for Ansible to work - tests should never deny/drop this connection (TCP 22/1222).

----

## Run

You can run the tests simply by running the script: `bash scripts/test.sh`

Parameters you add to the test-script execution will be passed to `ansible-playbook`

Examples:

* Enable difference-mode: `bash scripts/test.sh -D`
* Limit the execution: `bash scripts/test.sh --limit=container`
* Only test one module: `bash scripts/test.sh -e=test_module=list`

If a testing fails you might need/want to run the cleanup: `bash scripts/test_cleanup.sh`
