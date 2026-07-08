# Practice Guide: Chapter 23

## Objective
To interpret the `uptime` output, accurately read system memory, and navigate the interactive `top` interface.

## Assignment 1: The Health Check
Let's see how your virtual machine is feeling today.

1. Run the system uptime command:
   `uptime`
2. Look at the three numbers at the far right:
   * What is the 1-minute load?
   * What is the 15-minute load?
   * *(Unless you are actively compiling software, these numbers should be very close to 0.00).*
3. Run the memory check:
   `free -h`
4. Look at the output:
   * Look at the `free` column. It might look surprisingly low.
   * Look at the `buff/cache` column. This is the RAM Linux is "borrowing" to make your hard drive faster.
   * Look at the `available` column. This is the true metric. This is how much RAM you actually have left to run new programs.

## Assignment 2: The Process Monitor
Let's dive into the live task manager.

1. Launch the top interface:
   `top`
2. **Do not press any keys yet.** Just watch the screen. Notice that it refreshes every 3 seconds.
3. Look at the top row. It contains the exact same information as the `uptime` command you just ran!
4. Look at the fourth row (`KiB Mem`). It contains the exact same information as the `free` command you just ran!
5. Now, interact with the interface:
   * Press `M` (Capital M). The list is now sorted by the programs using the most RAM.
   * Press `P` (Capital P). The list is now sorted by the programs using the most CPU.
6. Look at the `USER` column. You will see some processes owned by `root`, and some owned by your username.
7. Look at the `COMMAND` column on the far right. Can you find the process called `top`? (It should be near the top because it requires CPU to draw the screen!).
8. Exit the interface by pressing `q`.

## Success Criteria
You have successfully completed this practice if you read your Load Average, identified your true `available` memory, launched `top`, sorted it by CPU and Memory, and successfully exited the program.
