# Practice Guide: Chapter 20 (Volume 4)

## Objective
To theoretically calculate and evaluate Disaster Recovery metrics (RTO and RPO) based on business requirements.

## Assignment 1: The E-Commerce Platform
You are the Lead Engineer for a major e-commerce platform that processes $100,000 in sales every hour. 

The CEO provides you with the following business requirements for a disaster scenario (e.g., the primary datacenter burns to the ground):
1. "We cannot afford to be offline for more than 4 hours, or the brand damage will be permanent."
2. "We cannot afford to lose more than 15 minutes of customer order data."

## Assignment 2: Metric Translation
Translate the CEO's requirements into technical DR metrics.

1. **What is the RTO (Recovery Time Objective)?**
   * *Answer:* 4 Hours. You have exactly 4 hours to provision new servers, restore the database, and update the DNS records.
2. **What is the RPO (Recovery Point Objective)?**
   * *Answer:* 15 Minutes.

## Assignment 3: Architectural Design
Based on the metrics above, evaluate the following two proposed architectures.

**Architecture A (The Cheap Option):**
* Infrastructure is provisioned manually by clicking around the AWS Console (Takes 6 hours).
* The database is backed up to Amazon S3 once every night at midnight.

**Architecture B (The Enterprise Option):**
* Infrastructure is provisioned automatically using Terraform and a CI/CD pipeline (Takes 15 minutes).
* The database asynchronously replicates every single transaction to a read-replica in a backup region with a 5-second delay.

**Analysis:**
1. Does Architecture A meet the RTO? 
   * *No. The RTO is 4 hours, but manual provisioning takes 6 hours.*
2. Does Architecture A meet the RPO?
   * *No. The RPO is 15 minutes, but backups only happen every 24 hours. If the datacenter burns down at 11:59 PM, you lose 23 hours and 59 minutes of orders!*
3. Does Architecture B meet the RTO and RPO?
   * *Yes. The Terraform deployment (15 mins) is well under the 4-hour RTO. The database replication delay (5 seconds) is well under the 15-minute RPO.*

## Success Criteria
You have successfully completed this practice if you understand that Disaster Recovery is not a purely technical problem; it is a business decision where the acceptable amount of downtime and data loss directly dictates the complexity and cost of the engineering architecture.
