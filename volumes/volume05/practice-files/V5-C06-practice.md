# Practice Guide: Chapter 6 (Volume 5)

## Objective
To write an advanced Bash script that uses `set -e`, parses command-line arguments using `getopts`, and extracts data using `awk`.

## Assignment 1: The Basic Script Skeleton
We will write a script that analyzes an NGINX access log to find the top IP addresses causing 404 Not Found errors. 

1. Open a new file: `nano log_analyzer.sh`

2. Define the strict mode and a help function:

    ```bash
    #!/bin/bash
    set -euo pipefail

    usage() {
        echo "Usage: $0 -f <log_file> -t <top_count>"
        echo "  -f : Path to the NGINX access log"
        echo "  -t : Number of top IPs to display (default: 5)"
        exit 1
    }
    ```

## Assignment 2: Parsing Arguments with `getopts`
Senior scripts do not use hardcoded paths. We want the user to run `./log_analyzer.sh -f /var/log/nginx/access.log -t 10`.

1. Append the following argument parsing block:

    ```bash
    LOG_FILE=""
    TOP_COUNT=5 # Default value

    while getopts "f:t:h" opt; do
        case ${opt} in
            f ) LOG_FILE="$OPTARG" ;;
            t ) TOP_COUNT="$OPTARG" ;;
            h ) usage ;;
            * ) usage ;;
        esac
    done

    # Validate that the user actually provided a file
    if [[ -z "$LOG_FILE" ]]; then
        echo "ERROR: -f <log_file> is required." >&2
        usage
    fi

    # Validate that the file actually exists
    if [[ ! -f "$LOG_FILE" ]]; then
        echo "ERROR: File '$LOG_FILE' does not exist." >&2
        exit 1
    fi
    ```

## Assignment 3: Data Extraction with `awk`
Now we process the file. A standard NGINX log separates data by spaces. The IP address is Column 1 (`$1`). The HTTP Status code (e.g., 200, 404) is Column 9 (`$9`).

1. Append the core logic:

    ```bash
    echo "Analyzing $LOG_FILE for the top $TOP_COUNT IPs causing 404 errors..."

    # 1. Use awk to filter only lines where column 9 is "404"
    # 2. Print column 1 (the IP)
    # 3. Sort the IPs
    # 4. Count the unique occurrences (uniq -c)
    # 5. Sort them numerically descending (sort -nr)
    # 6. Use head to grab the top X results

    awk '$9 == "404" {print $1}' "$LOG_FILE" \
        | sort \
        | uniq -c \
        | sort -nr \
        | head -n "$TOP_COUNT"
    ```

2. Save the script and make it executable: `chmod +x log_analyzer.sh`

## Success Criteria
You have successfully completed this practice if you can explain why `if [[ ! -f "$LOG_FILE" ]]; then` is a critical safety check. (Answer: Without it, the `awk` command would fail trying to read a non-existent file, and because we use `set -e`, the script would instantly crash and throw an ugly system error. It is always better to catch the error manually and print a helpful, human-readable error message!).
