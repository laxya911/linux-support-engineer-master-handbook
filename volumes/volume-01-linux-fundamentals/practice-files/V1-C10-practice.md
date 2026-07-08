# Practice Guide: Chapter 10

## Objective
To build muscle memory for safely syncing the package cache, searching for packages, and managing installations using both `apt` and `dnf` syntax.

## Assignment 1: Syncing the Cache
Before installing anything, always ensure your local package database knows about the latest upstream releases.

1. Log into your virtual machine.
2. Depending on your distribution, update the cache:
   * **Ubuntu 26.04**: `sudo apt update`
   * **RHEL 10 / CentOS**: `sudo dnf check-update`
3. Notice the output. It will tell you how many packages are available for an upgrade.

## Assignment 2: The Installation Lifecycle
We are going to install `htop`, a popular interactive process viewer.

1. **Search**: Verify the package actually exists.
   * Ubuntu: `apt search htop`
   * RHEL: `dnf search htop`
2. **Install**: Install the package. Notice that it will ask you to confirm (`Y/n`) because it calculates how much disk space it will consume.
   * Ubuntu: `sudo apt install htop`
   * RHEL: `sudo dnf install htop`
3. **Verify**: Run the program by typing `htop`. You should see a colorful dashboard of your CPU and RAM.
4. Press `q` to quit `htop`.

## Assignment 3: The Purge
You no longer need `htop`. We will completely remove it from the system.

1. **Remove**:
   * Ubuntu: `sudo apt purge htop`
   * RHEL: `sudo dnf remove htop`
2. Try running `htop` again. You should receive a `command not found` error.

## Success Criteria
You have successfully completed this practice if you were able to install `htop`, run it to view your system metrics, and then completely wipe it from the server without error.
