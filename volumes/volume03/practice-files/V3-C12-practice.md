# Practice Guide: Chapter 12 (Volume 3)

## Objective
To conceptually analyze a Linux DHCP server configuration file and understand how it distributes leases.

## Assignment 1: Analyzing the Configuration
Read the following theoretical `dhcpd.conf` file:

```text
# Global Parameters
default-lease-time 43200; # 12 hours
max-lease-time 86400;     # 24 hours
option domain-name "office.company.local";
option domain-name-servers 8.8.8.8, 1.1.1.1;

# The Main Office Subnet
subnet 10.0.5.0 netmask 255.255.255.0 {
  range 10.0.5.100 10.0.5.250;
  option routers 10.0.5.1;
}

# The HR Server Reservation
host hr-database {
  hardware ethernet 52:54:00:12:34:56;
  fixed-address 10.0.5.10;
}
```

**Answer the following questions:**
1. If an employee connects their iPhone to the Wi-Fi, what IP address range might it receive?
   *(Answer: It will receive an IP between 10.0.5.100 and 10.0.5.250).*
2. What IP address is the default gateway (the router) that the iPhone will use to reach the internet?
   *(Answer: 10.0.5.1).*
3. The HR database server has a reserved IP. Why is it safe from causing an IP conflict?
   *(Answer: Because its fixed-address, 10.0.5.10, is outside the 100-250 dynamic range pool).*

## Assignment 2: The Leases File
When a DHCP server gives away an IP, it records the transaction in a `.leases` file so it doesn't forget. 

Read the following theoretical lease entry:
```text
lease 10.0.5.105 {
  starts 2 2026/07/07 08:30:00;
  ends 2 2026/07/07 20:30:00;
  hardware ethernet a1:b2:c3:d4:e5:f6;
  client-hostname "John-MacBook-Pro";
}
```

**Answer the following questions:**
1. Who currently owns the IP `10.0.5.105`?
   *(Answer: John's MacBook Pro).*
2. How long is the lease valid for?
   *(Answer: 12 hours, which matches our `default-lease-time` of 43200 seconds!).*

## Success Criteria
You have successfully completed this practice if you correctly identified the dynamic pool range, default gateway, and fixed-address reservation in a standard DHCP configuration file.
