# Practice Guide: Chapter 16 (Volume 2)

## Objective
To write a Bash script utilizing a `for` loop, a variable, and an `if/else` conditional block based on Exit Codes.

## Assignment 1: Writing the Script
We are going to write a script that attempts to ping three famous DNS servers.

1. Create a new file in your home directory:
   `nano ~/ping_test.sh`
2. Write the following code into the file (pay close attention to spaces!):
   ```bash
   #!/bin/bash
   
   # Define the servers we want to test
   SERVERS="8.8.8.8 1.1.1.1 256.256.256.256"
   
   # Loop through each server
   for IP in $SERVERS; do
       echo "Pinging $IP..."
       
       # Ping the IP exactly 1 time, and hide the output by sending it to /dev/null
       ping -c 1 $IP > /dev/null 2>&1
       
       # Check the Exit Code of the ping command
       if [ $? -eq 0 ]; then
           echo "  -> SUCCESS: $IP is online."
       else
           echo "  -> FAILED: $IP is offline."
       fi
   done
   ```
3. Save the file and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

## Assignment 2: Executing the Script
If you try to run the script right now by typing `./ping_test.sh`, you will get a "Permission denied" error.

1. Make the script executable:
   `chmod +x ~/ping_test.sh`
2. Run the script:
   `./ping_test.sh`
3. **Observation:** 
   * The script will pause while it attempts to ping each IP.
   * `8.8.8.8` (Google) and `1.1.1.1` (Cloudflare) should report SUCCESS.
   * `256.256.256.256` is an invalid IP address. The `ping` command will fail in the background, returning a non-zero exit code. Our `if/else` statement will detect this failure and print FAILED.

## Success Criteria
You have successfully completed this practice if your script successfully executed, looped through all three IP addresses, and correctly identified the invalid IP address using the `$?` exit code variable.
