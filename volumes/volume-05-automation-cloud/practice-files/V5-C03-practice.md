# Practice Guide: Chapter 3 (Volume 5)

## Objective
To conceptually design an AWS S3 Bucket Lifecycle Configuration using Terraform to automate data tiering and reduce storage costs.

## Assignment 1: The S3 Bucket
First, we must define the S3 bucket where our compliance log files will be stored.

1. Open a new file:
   `nano s3-lifecycle.tf`
2. Write the theoretical Terraform code to create a private bucket:
   ```hcl
   resource "aws_s3_bucket" "compliance_logs" {
     bucket = "company-compliance-logs-2026"
   }

   resource "aws_s3_bucket_acl" "compliance_logs_acl" {
     bucket = aws_s3_bucket.compliance_logs.id
     acl    = "private"
   }
   ```

## Assignment 2: The Lifecycle Rule
The business requires that log files are immediately accessible for 30 days. After 30 days, they are rarely looked at, but must be kept for 7 years (2555 days) for legal reasons. We do not want to pay `Standard` storage prices for 7 years!

1. Append the following block to your file to create the automation rule:
   ```hcl
   resource "aws_s3_bucket_lifecycle_configuration" "log_tiering" {
     bucket = aws_s3_bucket.compliance_logs.id

     rule {
       id     = "archive_old_logs"
       status = "Enabled"

       filter {
         prefix = "logs/" # Only apply this rule to files inside the 'logs/' folder
       }

       # Move to Infrequent Access after 30 days
       transition {
         days          = 30
         storage_class = "STANDARD_IA"
       }

       # Move to Deep Archive (Cold Storage) after 90 days
       transition {
         days          = 90
         storage_class = "DEEP_ARCHIVE"
       }

       # Delete the files permanently after 7 years (2555 days)
       expiration {
         days = 2555
       }
     }
   }
   ```

## Assignment 3: The Financial Analysis
1. **Analysis:** Let's assume you store 100 Terabytes of logs.
2. If you left them in S3 Standard forever, it would cost roughly **$2,300 per month**.
3. By applying this Terraform code, the files automatically move to `STANDARD_IA` on day 30, dropping the price to roughly **$1,250 per month**.
4. On day 90, the files move to `DEEP_ARCHIVE`. The price plummets to roughly **$99 per month**. 
5. Over the required 7-year retention period, this simple block of code saves the business nearly **$180,000**. 

## Success Criteria
You have successfully completed this practice if you can look at the Terraform `transition` blocks and explain exactly when a file will be moved to cold storage, and when it will be permanently deleted.
