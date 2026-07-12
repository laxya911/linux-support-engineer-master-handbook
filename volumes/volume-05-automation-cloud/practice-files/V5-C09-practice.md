# Practice Guide: Chapter 9 (Volume 5)

## Objective
To write a Python script using the `boto3` library that searches for running EC2 instances tagged as "Development" and stops them to save costs.

## Assignment 1: Initializing Boto3
We must import the library and create a client object to interact with the EC2 service.

1. Create a Python Virtual Environment and install the library:
   `pip install boto3`

2. Open a new file: `nano auto_stop.py`

3. Write the initialization code:

    ```python
    import boto3
    import sys

    # Create the low-level EC2 client. 
    # Boto3 will automatically find your credentials in ~/.aws/credentials or IAM!
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    ```

## Assignment 2: Querying the API
We do not want to stop *all* instances, only the running development ones. We will use the API's built-in filtering mechanisms.

1. Append the following logic:

    ```python
    print("Scanning AWS for running Development instances...")

    # 1. Define the filters (State = running, Tag:Environment = Development)
    filters = [
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        },
        {
            'Name': 'tag:Environment',
            'Values': ['Development']
        }
    ]

    # 2. Call the API
    response = ec2_client.describe_instances(Filters=filters)

    # 3. Parse the JSON Dictionary response
    instances_to_stop = []
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instances_to_stop.append(instance_id)
            print(f"Found target instance: {instance_id}")
    ```

## Assignment 3: Executing the Action
Now that we have a Python List containing the Instance IDs, we can pass that list back to AWS to stop them simultaneously.

1. Append the execution logic:

    ```python
    # 4. Check if we found anything
    if not instances_to_stop:
        print("No running development instances found. Exiting.")
        sys.exit(0)

    # 5. Stop the instances!
    print(f"Attempting to stop {len(instances_to_stop)} instances...")
    
    try:
        stop_response = ec2_client.stop_instances(InstanceIds=instances_to_stop)
        
        # 6. Verify the API accepted the command
        for stopped_instance in stop_response['StoppingInstances']:
            print(f"Successfully sent stop command to: {stopped_instance['InstanceId']}")
            
    except Exception as e:
        print(f"Error stopping instances: {e}")
        sys.exit(1)
    ```

## Assignment 4: Theoretical Execution

1. A cronjob runs `python3 auto_stop.py` on Friday at 6:00 PM.

2. Boto3 creates an HTTP GET request to `ec2.us-east-1.amazonaws.com/?Action=DescribeInstances`.

3. Boto3 signs the request with your secure IAM token.
4. AWS returns a massive JSON payload containing 5 development instances.
5. Python parses the JSON, extracts the 5 IDs into a list: `['i-0123', 'i-0456', ...]`.
6. Boto3 creates a new HTTP POST request to `?Action=StopInstances` containing the 5 IDs.
7. AWS stops the virtual machines, immediately halting their hourly billing cycle. 

## Success Criteria
You have successfully completed this practice if you can explain why we used the `Filters` parameter in `describe_instances()` rather than pulling *all* instances and doing the filtering in Python. (Answer: Pulling all 10,000 company instances over the internet just to find 5 is incredibly slow and wastes bandwidth. It is always better to push the filtering logic to the AWS server-side API so it only sends back exactly what you need!).
