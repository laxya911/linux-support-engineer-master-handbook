# Practice Guide: Chapter 6 (Volume 4)

## Objective
To install the Terraform CLI, write a basic `main.tf` file using the `local` provider, and execute the standard Terraform workflow.

## Assignment 1: Installation
Terraform is a single binary executable written in Go, making it incredibly easy to install.

1. Download the latest binary for Linux:
   `curl -LO "https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip"`
2. Unzip it (install `unzip` if necessary: `sudo apt install unzip`):
   `unzip terraform_1.5.7_linux_amd64.zip`
3. Move the binary to your system's PATH:
   `sudo mv terraform /usr/local/bin/`
4. Verify the installation:
   `terraform version`

## Assignment 2: Writing the Code
Instead of using AWS (which requires API keys), we will use the `local` provider. This provider simply creates files on your local hard drive, but the workflow is exactly the same as managing cloud resources!

1. Create a dedicated directory:
   `mkdir ~/terraform-practice && cd ~/terraform-practice`
2. Create your main configuration file:
   `nano main.tf`
3. Paste the following HCL (HashiCorp Configuration Language) code:
   ```hcl
   terraform {
     required_providers {
       local = {
         source = "hashicorp/local"
         version = "2.4.0"
       }
     }
   }

   resource "local_file" "my_server_config" {
     filename = "${path.module}/server_config.txt"
     content  = "This file was provisioned automatically by Terraform!"
   }
   ```
4. Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

## Assignment 3: The Terraform Workflow
There are three core commands you will run every time you use Terraform.

1. **Initialize:** Download the required provider plugins (in this case, the `local` provider).
   `terraform init`
2. **Plan:** Ask Terraform to compare the code against reality and tell you what it *intends* to do. (It will state `Plan: 1 to add`).
   `terraform plan`
3. **Apply:** Tell Terraform to execute the plan and create the resource.
   `terraform apply`
   *(Type `yes` when prompted).*

## Assignment 4: Verification and The State File
Let's see what Terraform actually did behind the scenes.

1. Verify the resource was created:
   `cat server_config.txt`
2. Now, look at the files in your directory:
   `ls -a`
3. **Observation:** You will see a `terraform.tfstate` file! Open it:
   `cat terraform.tfstate`
4. **Result:** You are looking at the JSON representation of the State. This is how Terraform remembers that it owns `server_config.txt`.

## Assignment 5: Cleanup
1. Tell Terraform to destroy everything it created in the `main.tf` file:
   `terraform destroy`
   *(Type `yes` when prompted).*
2. Verify the file is gone:
   `ls server_config.txt` (It should say No such file or directory).

## Success Criteria
You have successfully completed this practice if you executed the `init`, `plan`, and `apply` workflow, verified the creation of the `.tfstate` file, and successfully executed a `destroy` to clean up the resources.
