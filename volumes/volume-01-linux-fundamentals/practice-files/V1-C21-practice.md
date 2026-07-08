# Practice Guide: Chapter 21

## Objective
To simulate a broken software installation and fix it by modifying the `$PATH` environment variable.

## Assignment 1: The Broken Software
We are going to create a script in a custom directory.

1. Create a custom folder in your home directory:
   `mkdir ~/custom_tools`
2. Create a basic script inside that folder:
   `echo 'echo "The custom tool is working!"' > ~/custom_tools/mytool`
3. Make it executable:
   `chmod +x ~/custom_tools/mytool`
4. Now, go to your home directory:
   `cd ~`
5. Try to run the tool by just typing its name:
   `mytool`
6. **Result:** You will get `bash: mytool: command not found`. Linux does not know it exists.

## Assignment 2: The Temporary Fix
Let's tell Linux where to look.

1. View your current PATH:
   `echo $PATH`
   *(Notice that `/home/youruser/custom_tools` is nowhere in that list).*
2. Append your new folder to the PATH:
   `export PATH=$PATH:~/custom_tools`
3. View your PATH again:
   `echo $PATH`
   *(Notice your folder is now appended to the very end of the list).*
4. Try to run the tool again:
   `mytool`
5. **Result:** It works! The terminal prints "The custom tool is working!"

## Assignment 3: The Permanent Fix
If you close your terminal right now, it will break again. Let's make it permanent.

1. Open your bash configuration file:
   `nano ~/.bashrc`
2. Scroll to the absolute bottom of the file (using the Down Arrow or Page Down).
3. Add your export command on a new line at the bottom:
   `export PATH=$PATH:~/custom_tools`
4. Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).
5. Close your terminal, open a new terminal, and type `mytool`. It will survive the reboot!

## Success Criteria
You have successfully completed this practice if you encountered the "command not found" error, fixed it temporarily using `export`, and then hardcoded the fix into your `~/.bashrc` file.
