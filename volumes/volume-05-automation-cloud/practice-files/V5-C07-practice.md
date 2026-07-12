# Practice Guide: Chapter 7 (Volume 5)

## Objective
To write a Python script that bridges the gap between Python and Linux by using the `subprocess` module to execute the `df -h` command, capture the output, and parse it.

## Assignment 1: Executing a Linux Command in Python
We want to check if the root filesystem `/` is full, but we want to do the math and alerting in Python.

1. Open a new file: `nano disk_monitor.py`

2. Write the following code to run `df -h /`:

    ```python
    #!/usr/bin/env python3
    import subprocess
    import sys

    # 1. Define the command as a list (for security)
    command = ["df", "-h", "/"]

    # 2. Execute the command and capture the output
    try:
        result = subprocess.run(
            command, 
            capture_output=True, # We want to capture the text, not just print it to the screen
            text=True,           # Decode the bytes into a string
            check=True           # Throw a Python Exception if the command fails (e.g. invalid path)
        )
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        sys.exit(1)
    ```

## Assignment 2: Parsing the Output
The `result.stdout` variable now contains the raw text output of the `df` command. It looks like this:
```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p1   20G   15G  5.0G  75% /
```
We need to extract the "75%".

1. Append the parsing logic to your script:

    ```python
    # 3. Get the raw text
    raw_output = result.stdout

    # 4. Split the text into lines, and grab the second line (index 1)
    data_line = raw_output.strip().split('\n')[1]

    # 5. Split that line by spaces, and grab the 5th column (index 4)
    # data_line.split() automatically handles multiple spaces!
    usage_string = data_line.split()[4] 

    # 6. Remove the '%' sign and convert to an Integer
    usage_percent = int(usage_string.replace('%', ''))

    print(f"Current Root Disk Usage: {usage_percent}%")

    # 7. Alerting Logic
    if usage_percent > 90:
        print("CRITICAL: Disk space is critically low!")
        # (Theoretical) Here you would use the 'requests' module to send a Slack alert
        sys.exit(2)
    else:
        print("OK: Disk space is healthy.")
        sys.exit(0)
    ```

## Assignment 3: Theoretical Execution

1. You run `python3 disk_monitor.py`.

2. Python reaches out to the Linux kernel and asks it to execute `/bin/df -h /`.

3. Linux executes it and returns the text to Python.
4. Python splits the text into arrays, grabs the specific word, strips the `%` sign, and turns it into a mathematical Integer.
5. Python evaluates `if 75 > 90`, prints "OK", and exits with status 0.

## Success Criteria
You have successfully completed this practice if you can explain why we passed the command as a list `["df", "-h", "/"]` instead of a string `"df -h /"`. 
(Answer: Passing a list avoids using the system shell, which prevents Shell Injection attacks. If a user provided the path, and we used a string, they could pass `/; rm -rf /`, and Python would blindly execute it!).
