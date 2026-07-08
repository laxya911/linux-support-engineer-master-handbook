# Practice Guide: Chapter 4

## Objective
To simulate an emergency recovery scenario by interrupting the bootloader (GRUB2) and forcing the Kernel to boot into a root shell without requiring a password.

## Assignment 1: Emergency Boot Override

Imagine you are locked out of your server. You lost the `root` password, and no other users have `sudo` privileges. You must interrupt the boot process to regain control.

> [!CAUTION]
> Do not perform this on a production server without authorization. This lab should only be done on the Virtual Machine you provisioned in Chapter 1.

### Step 1: Interrupt GRUB
1. Reboot your virtual machine.
2. The moment the VM starts to boot, hold the **Shift** key (on Ubuntu) or press the **Esc** key repeatedly (on RHEL/CentOS) to force the GRUB menu to appear.
3. Use the arrow keys to highlight the default boot entry.
4. Press `e` to edit the boot parameters.

### Step 2: Modify the Kernel Line
You are now viewing the GRUB configuration temporarily loaded into RAM. Scroll down to the line that begins with `linux` or `linux16` (this is the line that executes the Kernel).

Follow the instructions for your specific distribution:

> **Debian/Ubuntu 26.04**: 
> Move your cursor to the very end of the `linux` line. Add a space, and append the following:
> `systemd.unit=emergency.target`

> **RHEL 10 / CentOS Stream**:
> Move your cursor to the very end of the `linux` line. Add a space, and append the following:
> `rd.break`

### Step 3: Boot the System
Press `Ctrl + X` (or `F10`) to boot the system with your modified parameters.

## Success Criteria
You have successfully completed this practice if your boot sequence halts and drops you into a plain-text terminal ending in `#` (a root shell). 

If you were successfully dropped into this shell, you have essentially bypassed the Phase 4 init sequence (which would normally ask for a password) and told the system to stop booting immediately after Phase 3. 

*To exit the lab, simply type `reboot -f` to force a reboot back to normal operations.*
