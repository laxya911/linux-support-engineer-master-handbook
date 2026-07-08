# Practice Guide: Chapter 7 (Volume 4)

## Objective
To conceptually configure a Terraform Remote Backend and write a reusable module utilizing input variables.

## Assignment 1: The Remote Backend Configuration
We will write the standard configuration block used by almost every enterprise on AWS to secure their state file.

1. Open a blank text file:
   `nano backend.tf`
2. Write the theoretical configuration block. Notice how we specify both the S3 bucket (for storage) and the DynamoDB table (for locking):
   ```hcl
   terraform {
     backend "s3" {
       bucket         = "company-production-terraform-state"
       key            = "vpc/terraform.tfstate"
       region         = "us-east-1"
       encrypt        = true
       dynamodb_table = "terraform-state-lock"
     }
   }
   ```
3. Save and close the file. In a real environment, running `terraform init` in this directory would instantly connect to AWS and lock down the state!

## Assignment 2: Using Input Variables
Hardcoding is the enemy of automation. Let's write a module that deploys an EC2 instance, but uses variables so it can be reused for Dev, Staging, and Prod.

1. Open a new file for variables:
   `nano variables.tf`
2. Define an input variable. We will provide a default value just in case the engineer forgets to specify one!
   ```hcl
   variable "instance_size" {
     description = "The size of the EC2 instance to deploy."
     type        = string
     default     = "t2.micro"
   }
   ```
3. Save and close the file.

## Assignment 3: Writing the Resource
Now we write the actual compute resource, injecting our variable into it.

1. Open your main configuration file:
   `nano main.tf`
2. Paste the following AWS provider and resource configuration:
   ```hcl
   provider "aws" {
     region = "us-east-1"
   }

   resource "aws_instance" "web_server" {
     ami           = "ami-0c55b159cbfafe1f0" # Ubuntu 20.04
     instance_type = var.instance_size
     
     tags = {
       Name = "Production-Web-Server"
     }
   }
   ```
3. Save and close the file. Notice `instance_type = var.instance_size`. 

## Assignment 4: The Theoretical Execution
If you had AWS credentials configured on your laptop, you could execute this code!

1. To deploy the default tiny instance (`t2.micro`), you would simply run:
   `terraform apply`
2. To deploy a massive production instance without touching your `main.tf` code, you would override the variable at runtime via the CLI:
   `terraform apply -var="instance_size=t3.xlarge"`

## Success Criteria
You have successfully completed this practice if you can conceptually explain how the `backend.tf` file prevents team conflicts, and how `variables.tf` allows a single Terraform resource block to deploy different sizes of infrastructure based on the environment!
