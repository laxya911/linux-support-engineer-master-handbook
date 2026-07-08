# Practice Guide: Chapter 1

## Objective
To simulate the initial setup required by a Linux Support Engineer and develop an operational mindset.

## Assignment 1: Mindset Shift
Write down three scenarios where a GUI (Graphical User Interface) would be actively detrimental to a production server environment. Explain why using the CLI is preferred.

## Assignment 2: Lab Provisioning
1. Choose your environment: 
   * A local hypervisor (VirtualBox, Hyper-V).
   * A standalone hypervisor (Proxmox).
   * A Cloud VM (AWS, Azure, Oracle Cloud).
2. Download an ISO for either **Ubuntu Server LTS** (Debian-based) or **Rocky Linux** (RHEL-based) if deploying locally.
3. Provision the Virtual Machine with the following specifications:
   * **RAM**: 2048 MB (2 GB)
   * **CPU**: 2 Cores
   * **Disk**: 20 GB (Dynamically Allocated)
4. Proceed through the installation steps.
   * **CRITICAL**: Do NOT install a desktop environment or GUI.

## Success Criteria
You have successfully completed this practice if you can boot the virtual machine and reach a plain-text `login:` prompt on a black screen.

> [!TIP]
> Keep this virtual machine. We will use it extensively in all upcoming chapters!
