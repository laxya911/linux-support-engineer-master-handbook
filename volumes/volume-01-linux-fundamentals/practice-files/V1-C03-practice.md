# Practice Guide: Chapter 3

## Objective
To understand how automated provisioning configurations are structured and to practice designing resilient storage layouts for enterprise servers.

## Assignment 1: Designing Storage Layouts
Imagine you are building two different production servers. For each server, decide which directories should be placed on their own dedicated partitions (e.g., `/var`, `/home`, `/tmp`, `/opt`).

1. **Web Server**: Hosts a static website, but generates a massive amount of HTTP access logs.
   * *Which directory needs its own partition to protect the OS?*
2. **Database Server**: Hosts a PostgreSQL database that is expected to grow by 50 GB per month. The database files are stored in `/var/lib/pgsql`.
   * *Which directory needs its own partition to protect the OS?*

**Write down your answers and explain your reasoning.**

## Assignment 2: Inspecting Cloud-init
Cloud-init uses a YAML configuration file to provision a server on its first boot. 

Read the following sample `cloud-init.yaml` snippet:

```yaml
#cloud-config
users:
  - name: supportadmin
    groups: sudo
    shell: /bin/bash
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    ssh_authorized_keys:
      - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ...

packages:
  - htop
  - nginx
  - curl

runcmd:
  - systemctl enable nginx
  - systemctl start nginx
```

**Task**: Based *only* on reading this file, write down what state the server will be in immediately after it finishes booting.
1. What user account is created?
2. Does the user need a password to run administrative commands?
3. What software will be pre-installed?
4. What service will be actively running?

## Success Criteria
You have successfully completed this practice if you can correctly identify the protective partitions needed for both server types, and accurately describe the final state of the cloud-init provisioned server.
