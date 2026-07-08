# Practice Guide: Chapter 11 (Volume 4)

## Objective
To conceptually design a Terraform configuration that creates an AWS Route53 Health Check and an Active-Passive failover DNS record.

## Assignment 1: The Health Check
Before Route53 can failover, it needs a Health Check to monitor the primary server. 

1. Open a new file:
   `nano dns-failover.tf`
2. Write the theoretical Terraform code for the Health Check. We will monitor our Primary Load Balancer on port 80.
   ```hcl
   resource "aws_route53_health_check" "primary_health" {
     ip_address        = "198.51.100.1" # Primary Datacenter IP
     port              = 80
     type              = "HTTP"
     resource_path     = "/healthz"
     failure_threshold = 3
     request_interval  = 10
     
     tags = {
       Name = "Primary-Datacenter-Check"
     }
   }
   ```
3. **Analysis:** This block tells AWS to hit `http://198.51.100.1/healthz` every 10 seconds. If it fails 3 times in a row (30 seconds), the health check flips to "Unhealthy".

## Assignment 2: The Primary Record (Active)
Now we create the DNS record for the Primary datacenter and link it to the Health Check.

1. Append the following block to your file:
   ```hcl
   resource "aws_route53_record" "primary_record" {
     zone_id = "Z123456789"
     name    = "www.company.com"
     type    = "A"
     ttl     = "60"
     
     set_identifier = "Primary-Active"
     failover_routing_policy {
       type = "PRIMARY"
     }
     
     health_check_id = aws_route53_health_check.primary_health.id
     records         = ["198.51.100.1"]
   }
   ```
2. **Analysis:** Notice the `ttl = 60`. If we set this to 86400 (24 hours), our failover would be useless! We also explicitly set this as the `PRIMARY` record.

## Assignment 3: The Secondary Record (Passive)
Finally, we define the Disaster Recovery datacenter. Route53 will *only* return this record if the Primary Health Check fails.

1. Append the final block to your file:
   ```hcl
   resource "aws_route53_record" "secondary_record" {
     zone_id = "Z123456789"
     name    = "www.company.com"
     type    = "A"
     ttl     = "60"
     
     set_identifier = "Secondary-Passive"
     failover_routing_policy {
       type = "SECONDARY"
     }
     
     # No health check needed for the secondary in a simple setup!
     records = ["203.0.113.5"] # Backup Datacenter IP
   }
   ```
2. Save and exit the file. 

## Success Criteria
You have successfully completed this practice if you can look at the Terraform code above and explain the exact sequence of events that occurs when the IP address `198.51.100.1` stops responding to HTTP requests.
