# Practice Guide: Chapter 8 (Volume 4)

## Objective
To install Ansible, create a local inventory file, and execute an ad-hoc module command.

## Assignment 1: Installation
Ansible is written in Python, so it is incredibly easy to install on any Linux system. You only need to install it on your "Control Node" (your laptop). 

1. **Ubuntu:**
   `sudo apt update && sudo apt install ansible`
2. **RHEL/CentOS:**
   `sudo dnf install epel-release`
   `sudo dnf install ansible`
3. Verify the installation:
   `ansible --version`

## Assignment 2: The Inventory
Ansible will not run unless you tell it *where* to run. For this practice, we will just use your own local VM as the target!

1. Create a dedicated directory:
   `mkdir ~/ansible-practice && cd ~/ansible-practice`
2. Create your inventory file:
   `nano inventory.ini`
3. We will create a group called `local` and add `localhost`. We also need to tell Ansible to use a "local" connection rather than trying to SSH out to the internet:
   ```ini
   [local]
   localhost ansible_connection=local
   ```
4. Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

## Assignment 3: Ad-Hoc Commands
Let's test the connection using the `ping` module. Unlike the bash `ping` command (which tests ICMP network packets), the Ansible `ping` module tests if Ansible can successfully execute Python code on the target machine!

1. Run the `ping` module against all servers in the `local` group, explicitly passing your inventory file (`-i`):
   `ansible local -i inventory.ini -m ping`
2. **Result:** You should see a green output stating `"ping": "pong"`. Ansible successfully verified it can manage your machine!

## Assignment 4: The Command Module
Let's run a raw bash command across the inventory.

1. Use the `command` module (`-m command`) and pass the command `uptime` as an argument (`-a "uptime"`):
   `ansible local -i inventory.ini -m command -a "uptime"`
2. **Result:** Ansible executes the uptime command and returns the string output to your screen! Imagine running that same command, but targeting a group of 500 servers instead of just localhost. That is the power of Ansible!

## Success Criteria
You have successfully completed this practice if you installed Ansible, created a valid `inventory.ini` file mapping to `localhost`, and successfully executed the `ping` and `command` modules via ad-hoc CLI commands.
