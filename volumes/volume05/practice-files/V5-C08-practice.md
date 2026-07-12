# Practice Guide: Chapter 8 (Volume 5)

## Objective
To write a Python script that leverages the `requests` library to send an HTTP POST request containing a JSON payload to a theoretical Slack Webhook URL.

## Assignment 1: Preparing the Environment
Because `requests` is a third-party library, we must install it safely.

1. Create a Python Virtual Environment:
   `python3 -m venv chatops_env`

2. Activate it:
   `source chatops_env/bin/activate`

3. Install the library:
   `pip install requests`

## Assignment 2: Writing the Bot
We want to send an alert that looks professional, using Slack's "Blocks" API to add formatting and emojis.

1. Open a new file: `nano slack_bot.py`

2. Write the Python code:

    ```python
    import requests
    import os
    import sys

    # 1. Safely retrieve the secret URL from an Environment Variable
    WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

    if not WEBHOOK_URL:
        print("ERROR: SLACK_WEBHOOK_URL environment variable is not set!")
        sys.exit(1)

    # 2. Build the JSON Payload dictionary
    # We are using Slack's specific schema here.
    payload = {
        "text": "Fallback text for older clients",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🚨 CRITICAL ALERT: Database Offline"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "The primary PostgreSQL database has stopped responding to pings on port 5432.\n*Server:* db-prod-01\n*Action Required:* Immediate investigation."
                }
            }
        ]
    }

    # 3. Send the POST Request
    print("Sending alert to Slack...")
    
    try:
        # The 'json=' parameter automatically converts the dictionary to a JSON string
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        
        # Force an exception if the HTTP code is 4xx or 5xx
        response.raise_for_status() 
        
        print("Alert successfully delivered!")
        
    except requests.exceptions.RequestException as e:
        print(f"Network or API Error while sending alert: {e}")
        sys.exit(1)
    ```

## Assignment 3: Theoretical Execution

1. A cronjob runs the script: `SLACK_WEBHOOK_URL="https://hooks.slack.com/..." python3 slack_bot.py`.

2. Python converts the complex `payload` dictionary into a raw JSON string.

3. Python initiates a TCP connection to `hooks.slack.com` on Port 443 (HTTPS).
4. Python sends the HTTP POST request.
5. Slack's API servers receive it, parse the JSON, and instantly render a beautifully formatted alert with a bold header into the chat room.
6. The `requests` library receives an `HTTP 200 OK` from Slack, and the script exits cleanly.

## Success Criteria
You have successfully completed this practice if you can explain what `response.raise_for_status()` does. (Answer: Instead of manually writing `if response.status_code != 200:`, this built-in function automatically throws a Python exception if the API returns an HTTP error code (like a 404 or 403), allowing the `except` block to catch it cleanly!).
