# Practice Guide: Chapter 9 (Volume 4)

## Objective
To write an Ansible Playbook using YAML, execute it to install a package, and prove Idempotency by running it a second time.

## Assignment 1: The Playbook
We will write a Playbook that targets our local machine. It will install the `wget` utility, but only if it isn't already installed!

1. Move to your Ansible practice directory:
   `cd ~/ansible-practice`
2. Ensure your `inventory.ini` file from Chapter 8 is still there!
3. Create the Playbook file:
   `nano setup.yml`
4. Paste the following YAML structure:
   ```yaml
   ---
   - name: Base Server Configuration
     hosts: local
     become: yes  # This tells Ansible to use sudo!
     
     tasks:
       - name: Ensure wget is installed
         package:
           name: wget
           state: present
       
       - name: Create a dummy config file
         copy:
           dest: /tmp/ansible-test.conf
           content: "This file was created by Ansible."
           mode: '0644'
         notify: Restart Dummy Service

     handlers:
       - name: Restart Dummy Service
         debug:
           msg: "The Handler was triggered because the file changed!"
   ```
5. Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

## Assignment 2: The First Execution (Changes Made)
Let's run the Playbook.

1. Execute the Playbook:
   `ansible-playbook setup.yml -i inventory.ini`
2. **Observation:** Ansible will output the status of each task. 
   * It will gather facts about your OS.
   * It will say `changed` for the `wget` task (assuming you didn't have it).
   * It will say `changed` for the `copy` task.
   * Because the `copy` task changed, it will say `RUNNING HANDLER [Restart Dummy Service]`.

## Assignment 3: Proving Idempotency
What happens if we immediately run the exact same Playbook again? Will it try to reinstall `wget` and overwrite the file?

1. Execute the exact same command again:
   `ansible-playbook setup.yml -i inventory.ini`
2. **Observation:** Look closely at the output!
   * The `wget` task says `ok` (Green), not `changed` (Yellow).
   * The `copy` task says `ok`.
   * **Crucial:** The Handler did NOT run! 
3. **Result:** Because Ansible is Idempotent, it checked the state of your machine, realized `wget` and the `/tmp/ansible-test.conf` file were already exactly as desired, and did absolutely nothing.

## Assignment 4: Simulating Configuration Drift
Let's pretend a rogue admin manually deletes the config file.

1. Manually delete the file:
   `rm /tmp/ansible-test.conf`
2. Run the Playbook one last time:
   `ansible-playbook setup.yml -i inventory.ini`
3. **Result:** Ansible detects the drift! It says `changed` for the copy task, replaces the missing file, and executes the Handler!

## Success Criteria
You have successfully completed this practice if you wrote a valid YAML playbook, ran it to observe state changes, and ran it a second time to definitively prove Idempotency and Handler logic.
