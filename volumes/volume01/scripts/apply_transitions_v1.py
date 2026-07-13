import os
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(os.path.dirname(script_dir), "chapters")

transitions = {
    "V1-C01": "You now understand the philosophy of support engineering, but to apply it, you must understand the environment. It is time to dissect the Linux architecture.",
    "V1-C02": "We've explored the architecture conceptually, but theory only goes so far. How do you actually get Linux running in the real world?",
    "V1-C03": "The server is provisioned, but what exactly happens between pressing the power button and seeing the login prompt?",
    "V1-C04": "The kernel is loaded and running, but where does it store all its configuration and data? Welcome to the Filesystem Hierarchy Standard.",
    "V1-C05": "You know where files are supposed to live. Now, how do you actually traverse the filesystem and manipulate them?",
    "V1-C06": "We can move and copy files, but as an engineer, your most important job is reading logs and editing configurations. You need a text editor.",
    "V1-C07": "You can edit files, but Linux is a multi-user system. How do you separate the administrators from the regular users?",
    "V1-C08": "Users exist, but how do we prevent Alice from deleting Bob's files? We must strictly define ownership and permissions.",
    "V1-C09": "Your permissions are set, but a system without software is just a very secure brick. How do we install the tools we need?",
    "V1-C10": "The software is installed and running. But when it misbehaves, how do you find and stop the rogue process?",
    "V1-C11": "Killing processes manually is tedious. How does Linux ensure critical services start automatically and stay running?",
    "V1-C12": "Systemd is managing the services, but when a service fails to start, how do you find out *why*? You must read the logs.",
    "V1-C13": "The local system is running perfectly, but a server is useless if it can't talk to the outside world. We must configure the network.",
    "V1-C14": "The server is on the network, but we can't physically walk to the data center every time we need to run a command. We need secure remote access.",
    "V1-C15": "We can connect remotely, but what about moving massive amounts of log data efficiently? We must compress and archive it.",
    "V1-C16": "Data is compressed, but eventually, you will run out of physical disk space. How do we manage storage at a block level?",
    "V1-C17": "Storage is mounted, but searching through gigabytes of logs manually is impossible. We need powerful text processing tools.",
    "V1-C18": "We can find the errors with grep, but how do we save those errors to a new file or chain commands together? Enter redirection and pipes.",
    "V1-C19": "Piping commands is great, but typing the same 5 commands every day is a waste of time. It's time to start scripting.",
    "V1-C20": "Scripts run sequentially, but how do they adapt to different users and system states dynamically? We must use environment variables.",
    "V1-C21": "Our scripts are dynamic and powerful. Now, how do we force the system to run them automatically at 3 AM?",
    "V1-C22": "The system is automating its own tasks, but how do we know if it's running out of RAM or CPU while we sleep?",
    "V1-C23": "We are monitoring the system, but what stops a malicious actor from exploiting our open ports? We need a basic firewall.",
    "V1-C24": "The firewall is active, but humans cannot remember IP addresses. How do we translate 'google.com' into an IP?",
    "V1-C25": "DNS is resolving names, but what happens when a critical service crashes on boot and the system won't start? Time to troubleshoot.",
    "V1-C26": "We can recover broken systems. Now, let's look at the most common workload you will support in your career: the web server.",
    "V1-C27": "A single web server is fine for a small site, but how do we handle millions of users across multiple backend servers?",
    "V1-C28": "The front-end traffic is balanced, but where do those web applications store their persistent data?",
    "V1-C29": "You've built the foundation from the boot process to database backends. So, where do you go from here?"
}

def apply_transitions():
    for filename in os.listdir(base_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(base_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 1. Clean up old generic transition
            content = re.sub(r'## Chapter Transition\n\nIn this chapter.*?## Navigation', '## Navigation', content, flags=re.DOTALL)
            # Remove any old Volume Transition blocks just in case
            content = re.sub(r'\*\*Chapter Transition\*\*.*?(?=---\s+## Navigation)', '', content, flags=re.DOTALL)
            
            # 2. Inject new custom transition
            chapter_id = filename[:6] # e.g. V1-C01
            if chapter_id in transitions:
                trans_text = transitions[chapter_id]
                new_block = f"**Chapter Transition**\n> {trans_text}\n\n---\n\n## Navigation"
                content = re.sub(r'## Navigation', new_block, content, count=1)
                
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    apply_transitions()
    print("Volume 1 transitions applied successfully.")
