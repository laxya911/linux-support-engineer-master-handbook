# Practice Guide: Chapter 2 (Volume 5)

## Objective
To conceptually design a Terraform configuration that creates a Launch Template and an Auto Scaling Group (ASG).

## Assignment 1: The Launch Template
The blueprint for our web servers. 

1. Open a new file:
   `nano asg-config.tf`

2. Write the theoretical Terraform code for the Launch Template. Notice the `user_data` script! This is the bash script that runs automatically when the VM boots up to install NGINX.

    ```hcl
    resource "aws_launch_template" "web_template" {
      name_prefix   = "web-server-template-"
      image_id      = "ami-0abcdef1234567890" # Amazon Linux 2026
      instance_type = "t3.micro"
      
      vpc_security_group_ids = ["sg-0123456789"]

      user_data = base64encode(<<EOF
        #!/bin/bash
        yum update -y
        yum install -y nginx
        systemctl enable --now nginx
        echo "Welcome to the Auto-Scaled Web Server!" > /usr/share/nginx/html/index.html
      EOF
      )
    }
    ```

3. **Analysis:** Every time the ASG decides to scale out, it will read this template, clone the `ami`, attach the `sg-0123456789` firewall, and run the `user_data` script to start NGINX.

## Assignment 2: The Auto Scaling Group
Now we create the ASG and tell it to use the template we just built.

1. Append the following block to your file:

    ```hcl
    resource "aws_autoscaling_group" "web_asg" {
      name                      = "production-web-asg"
      vpc_zone_identifier       = ["subnet-abc", "subnet-xyz"] # Two Availability Zones for HA
      
      desired_capacity          = 2
      min_size                  = 2
      max_size                  = 10
      
      target_group_arns         = ["arn:aws:elasticloadbalancing:region:account-id:targetgroup/my-targets/6d0ecf831eec9f09"]

      launch_template {
        id      = aws_launch_template.web_template.id
        version = "$Latest"
      }
    }
    ```

2. **Analysis:** 
   * `vpc_zone_identifier`: We place the ASG across two subnets in different datacenters. If one datacenter burns down, the ASG will instantly spin up new instances in the surviving datacenter!
   * `desired_capacity = 2`: The ASG will immediately ensure that exactly 2 web servers are running.
   * `max_size = 10`: The ASG is forbidden from spinning up more than 10 servers, protecting you from a massive AWS bill if a DDoS attack occurs!
   * `target_group_arns`: The ASG will automatically register the newly created VMs with this Load Balancer target group.

## Success Criteria
You have successfully completed this practice if you can explain why modifying the `user_data` script in the Launch Template will *not* magically update the EC2 instances that are already currently running in the ASG. (Answer: The Launch Template is only read when a *new* instance is provisioned. To update existing instances, you must use an 'Instance Refresh' to kill the old ones and spin up new ones!).
