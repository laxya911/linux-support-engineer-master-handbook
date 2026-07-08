# Practice Guide: Chapter 13 (Volume 3)

## Objective
To install a basic mail agent and send an email directly from the command line.

*(Note: Because your VM does not have a registered domain name or an SPF record, this email will almost certainly be flagged as Spam by your email provider. Check your Junk folder!)*

## Assignment 1: Installation
We need to install the `mail` command and the Postfix MTA (Mail Transfer Agent).

1. Install the utilities:
   * **Ubuntu/Debian:** `sudo apt update && sudo apt install mailutils`
   * **RHEL/CentOS:** `sudo dnf install mailx postfix`
2. If prompted by a pink Postfix configuration screen during installation, select **Internet Site** and press Enter. Accept the default "System mail name" and press Enter.

## Assignment 2: Sending the Email
Let's use the command line to craft a message.

1. Run the `mail` command, specifying your personal email address (e.g., your Gmail account):
   `mail -s "Test Email from Linux" your.name@gmail.com`
2. **Observation:** The terminal will drop to a blank line. It is waiting for you to type the body of the email!
3. Type the following:
   `Hello!`
   `This email was sent directly from my Linux terminal using SMTP!`
4. To finish the email and send it, press **Enter** to go to a new line, press **Ctrl+D**, and then press Enter again (to skip the CC field).

## Assignment 3: Checking the Logs
How do we know if it actually sent? We check the logs.

1. View the end of the mail log:
   `sudo tail -n 20 /var/log/mail.log` (Ubuntu) OR `/var/log/maillog` (RHEL)
2. **Observation:** You should see a line that says `status=sent`. This means Postfix successfully handed the email over to Google's servers!
3. Go check your personal email inbox. If it isn't there, check your Spam/Junk folder. It was likely flagged as spam because your VM does not have an SPF record!

## Success Criteria
You have successfully completed this practice if you installed Postfix, used the `mail` command to construct a message, successfully dispatched it, and verified the `status=sent` message in `/var/log/mail.log`.
