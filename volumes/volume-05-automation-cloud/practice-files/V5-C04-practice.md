# Practice Guide: Chapter 4 (Volume 5)

## Objective
To conceptually design the Terraform code that creates an AWS Transit Gateway and attaches a VPC to it.

## Assignment 1: The Transit Gateway (The Hub)
First, we must create the central routing Hub itself.

1. Open a new file:
   `nano transit-gateway.tf`

2. Write the theoretical Terraform code to create the TGW. We enable DNS support and specify a private ASN (Autonomous System Number) for BGP routing.

    ```hcl
    resource "aws_ec2_transit_gateway" "main_tgw" {
      description                     = "Global Corporate Transit Gateway"
      amazon_side_asn                 = 64512
      auto_accept_shared_attachments  = "enable"
      dns_support                     = "enable"
      
      tags = {
        Name = "Corporate-TGW"
      }
    }
    ```

## Assignment 2: The VPC Attachment (The Spoke)
Now we must attach our Production VPC to the central Hub.

1. Append the following block to your file. We tell the TGW which VPC to connect to, and which subnets within that VPC it should drop its Elastic Network Interfaces (ENIs) into.

    ```hcl
    resource "aws_ec2_transit_gateway_vpc_attachment" "prod_vpc_attach" {
      transit_gateway_id = aws_ec2_transit_gateway.main_tgw.id
      vpc_id             = "vpc-0abc123456789"
      
      # The TGW needs a foothold in at least one subnet per Availability Zone
      subnet_ids         = ["subnet-111111", "subnet-222222"] 
      
      tags = {
        Name = "Prod-VPC-Attachment"
      }
    }
    ```

## Assignment 3: The Route Table
Just because the VPC is *attached* to the TGW does not mean traffic will magically flow there. We must update the VPC's routing table to tell it to send on-premise traffic to the Hub.

1. Append the final block to your file. Our on-premise datacenter uses the `192.168.0.0/16` IP range.

    ```hcl
    resource "aws_route" "route_to_onprem" {
      route_table_id         = "rtb-0987654321" # The Route Table for the Prod VPC
      
      destination_cidr_block = "192.168.0.0/16"
      transit_gateway_id     = aws_ec2_transit_gateway.main_tgw.id
    }
    ```

2. **Analysis:** Let's trace the packet. 
   * An EC2 instance in the Prod VPC pings `192.168.5.50`.
   * The Linux kernel sends the packet to the VPC Route Table.
   * The Route Table matches `192.168.0.0/16` and forwards the packet to the Transit Gateway.
   * The Transit Gateway checks its own BGP routing table, sees the Site-to-Site VPN attachment for the on-premise datacenter, and forwards the packet through the encrypted tunnel to Chicago.

## Success Criteria
You have successfully completed this practice if you understand that network connectivity in AWS requires three distinct steps: Creating the Hub, Attaching the Spoke, and Explicitly updating the Route Tables!
