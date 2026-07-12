# Practice Guide: Chapter 20

## Objective
To write a bash script, observe the kernel blocking its execution, fix the permissions, and successfully run the code.

## Assignment 1: Writing the Script
1. Open a new file using your preferred text editor (like `nano` or `vim`):
   `nano hello.sh`
2. Type the mandatory Shebang on the very first line:
   `#!/bin/bash`
3. Add a blank line, and then type a command:
   `echo "Hello, World! My script is working!"`
4. Save and exit the file.

## Assignment 2: The Execution Failure
Let's simulate the most common mistake beginners make.

1. Try to run the script:
   `./hello.sh`
2. **Result:** You should receive a `bash: ./hello.sh: Permission denied` error.
3. Run `ls -l hello.sh` to see why.
   *Notice the permissions are likely `-rw-rw-r--`. There is no `x`.*

## Assignment 3: The Fix
1. Add the Execute permission to the file:
   `chmod +x hello.sh`
2. Run `ls -l hello.sh` again. 
   *Notice the permissions are now `-rwxrwxr-x`, and the filename might even be colored green in your terminal.*
3. Try to run the script again:
   `./hello.sh`
4. **Result:** The terminal prints your message!

## Assignment 4: Using Variables
Let's make the script slightly dynamic.

1. Open the file again: `nano hello.sh`
2. Modify the file to look exactly like this:
   ```bash
   #!/bin/bash
   
   CITY="New York"
   
   echo "Hello, World! I am running this script from $CITY."
   ```
3. Save and exit.
4. Run the script: `./hello.sh`
5. Verify the output correctly extracts the data from the `$CITY` variable.

## Success Criteria
You have successfully completed this practice if you were able to write a script, observe the permission denied error, fix it using `chmod +x`, and successfully utilize a dynamic variable.
