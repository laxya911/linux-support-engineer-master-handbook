# Practice Guide: Chapter 12

## Objective
To master the `systemctl` command by installing, monitoring, and managing the lifecycle of a real web server daemon.

## Assignment 1: The Installation
We need a service to manage. We will install the `nginx` web server.

1. Install the package:
   * **Ubuntu 26.04**: `sudo apt install nginx -y`
   * **RHEL 10 / CentOS**: `sudo dnf install nginx -y`
2. Once installed, ask `systemd` for a health check:
   `systemctl status nginx`
3. Look at the output. You should see two critical things:
   * It should say `Active: active (running)`.
   * It should say `Loaded: loaded (...; enabled; ...)`.
   *(Most package managers automatically start and enable the service upon installation).*

## Assignment 2: The Manual Lifecycle
Let's pretend the server is misbehaving and we need to turn it off.

1. Stop the web server:
   `sudo systemctl stop nginx`
2. Verify it is dead:
   `systemctl status nginx`
   *(It should now say `Active: inactive (dead)`).*
3. Now, disable it from starting on boot:
   `sudo systemctl disable nginx`
   *(Notice the output says it removed a symlink. You just detached it from the boot target).*
4. Run `systemctl status nginx` again. Look at the `Loaded` line. It should now say `disabled`.

## Assignment 3: The Recovery
We just simulated the "Real-World Scenario" from the chapter. The service is dead and will not survive a reboot. Let's fix it properly.

1. Run the ultimate command to fix both issues at once:
   `sudo systemctl enable --now nginx`
   *(This creates the symlink for boot, AND immediately starts the daemon).*
2. Verify the fix:
   `systemctl status nginx`
3. Press `q` to exit the status screen.

## Success Criteria
You have successfully completed this practice if you were able to install `nginx`, intentionally kill and disable it, and use the `--now` flag to simultaneously re-enable and restart the daemon.
