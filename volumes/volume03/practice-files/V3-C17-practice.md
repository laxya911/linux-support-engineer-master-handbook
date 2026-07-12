# Practice Guide: Chapter 17 (Volume 3)

## Objective
To simulate how Logstash and Kibana parse structured logs by using the `jq` command-line JSON processor.

## Assignment 1: The Raw JSON Log
Imagine an application is writing Structured JSON logs instead of plain text. 

1. Create a dummy log file named `app.log` in your home directory:
   `nano ~/app.log`
2. Paste the following three lines (representing three different events). Ensure each event is on one single line:
   ```json
   {"timestamp": "2026-07-08T10:00:00Z", "level": "INFO", "user": "Alice", "action": "login", "server": "web-01"}
   {"timestamp": "2026-07-08T10:05:00Z", "level": "ERROR", "user": "Bob", "action": "checkout", "server": "web-02", "error_code": 500}
   {"timestamp": "2026-07-08T10:10:00Z", "level": "INFO", "user": "Charlie", "action": "logout", "server": "web-01"}
   ```
3. Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

## Assignment 2: Using JQ (The Command-Line Kibana)
If you try to read that file with `cat`, it looks like a mess of brackets. We will use `jq` to parse it natively!

1. Install the `jq` utility:
   * **Ubuntu/Debian:** `sudo apt install jq`
   * **RHEL/CentOS:** `sudo dnf install jq`
2. Let's pretty-print the logs so they are readable by a human:
   `cat ~/app.log | jq '.'`
3. **Observation:** The `jq` tool automatically formatted the JSON with color-coding and proper indentation!

## Assignment 3: Filtering the Logs
Now let's extract specific data, proving why structured logging is better than Regex.

1. Let's say we only care about the Usernames that logged in today. Ask `jq` to extract *only* the `.user` field from all logs:
   `cat ~/app.log | jq '.user'`
2. **Observation:** It perfectly extracted "Alice", "Bob", and "Charlie".
3. Let's do a Kibana-style search! Find the exact log where the `level` is equal to `ERROR`:
   `cat ~/app.log | jq 'select(.level == "ERROR")'`
4. **Result:** It instantly isolates Bob's failed checkout on `web-02`! You just performed centralized log filtering using native JSON keys instead of messy `grep` commands!

## Success Criteria
You have successfully completed this practice if you created a JSON log file and used the `jq` utility to properly format the JSON and filter it by specific keys (like `.level`).
