# Practice Guide: Chapter 5 (Volume 5)

## Objective
To write a Bash script utilizing the `aws-cli` and `jq` to automate the discovery of "Zombie" unattached EBS (Elastic Block Store) volumes.

## Assignment 1: The AWS CLI Command
We need to query AWS for all volumes, but we only want the ones that are NOT attached to any server. 

1. The raw AWS CLI command to describe volumes is:
   `aws ec2 describe-volumes`

2. This returns a massive JSON document. We can use the AWS CLI's built-in `--query` parameter (which uses JMESPath syntax) to filter it.

3. We want to find volumes where the `Attachments` array is empty (meaning its status is `available` rather than `in-use`).
   `aws ec2 describe-volumes --filters Name=status,Values=available`

## Assignment 2: Formatting the Output with `jq`
The command above returns a lot of unnecessary data. We only want the Volume ID, the Size in GB, and the Type. We will pipe the JSON output into `jq` to make it readable.

1. Open a new file:
   `nano find-zombies.sh`

2. Write the following Bash script:

    ```bash
    #!/bin/bash

    echo "Hunting for unattached (Zombie) EBS Volumes..."
    echo "----------------------------------------------"

    # Run the AWS CLI and pipe the JSON into jq
    aws ec2 describe-volumes \
      --filters Name=status,Values=available \
      --output json | jq -r '.Volumes[] | "Volume ID: \(.VolumeId) | Size: \(.Size) GB | Type: \(.VolumeType)"'

    echo "----------------------------------------------"
    echo "Hunt complete. Please review these volumes for deletion to save money!"
    ```

3. Save and make the script executable:
   `chmod +x find-zombies.sh`

## Assignment 3: Theoretical Execution & Financial Analysis

1. Imagine you run `./find-zombies.sh` and it returns the following output:

    ```
    Volume ID: vol-0abcd123456789012 | Size: 500 GB | Type: gp3
    Volume ID: vol-0987654321fedcba0 | Size: 1000 GB | Type: io1
    ```

2. **Analysis:** The `gp3` storage costs roughly $0.08 per GB/month. That 500GB volume is wasting $40 a month.

3. The `io1` (Provisioned IOPS) storage is incredibly expensive, roughly $0.125 per GB/month *plus* a fee for the IOPS. That 1000GB volume is wasting well over $125 a month!
4. By deleting these two forgotten hard drives, you just saved the company almost $2,000 a year.

## Success Criteria
You have successfully completed this practice if you understand how to chain the AWS CLI with JSON parsers like `jq` to create actionable, money-saving automation scripts.
