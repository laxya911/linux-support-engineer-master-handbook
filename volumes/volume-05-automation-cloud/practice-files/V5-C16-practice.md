# Practice Guide: Chapter 16 (Volume 5)

## Objective
To practice "Back-of-the-Envelope" estimation, a critical skill for passing System Design interviews at top-tier tech companies.

## Assignment 1: The Traffic Estimation
**The Prompt:** The interviewer asks you to design a basic Twitter clone. They tell you the system has 100 Million Daily Active Users (DAU). 

1. **Calculate the Read/Write Ratio:**
   * Assume each user posts 2 tweets per day (200 Million writes per day).
   * Assume each user reads 100 tweets per day (10 Billion reads per day).
   * *Conclusion:* This is an extremely read-heavy system (50:1 read/write ratio). You must prioritize caching (Redis) in your design!

2. **Calculate Requests Per Second (RPS):**
   * There are 86,400 seconds in a day. (Round it to 100,000 for easy whiteboard math).
   * Write RPS: `200,000,000 / 100,000` = **2,000 Writes per second.**
   * Read RPS: `10,000,000,000 / 100,000` = **100,000 Reads per second.**

## Assignment 2: The Storage Estimation
Now that you know the traffic, you must determine how much hard drive space your database will need.

1. **Calculate the Size of a Single Tweet:**
   * Assume a tweet is mostly text (140 characters).
   * 1 character = 2 bytes. 
   * Add 100 bytes for metadata (Timestamp, User ID, Location).
   * Let's say a single tweet is roughly **400 Bytes**.

2. **Calculate Daily Storage Requirements:**
   * 200 Million tweets per day * 400 Bytes.
   * `200,000,000 * 400` = 80,000,000,000 Bytes = **80 Gigabytes per day.**

3. **Calculate 5-Year Storage Capacity:**
   * 80 GB per day * 365 Days = ~30 Terabytes per year.
   * 30 TB * 5 Years = **150 Terabytes.**

## Assignment 3: Architectural Decisions
Based on the numbers you just calculated on the whiteboard, you can now make definitive architectural choices!

1. **The Database Choice:** A single PostgreSQL database can easily handle 2,000 writes per second. However, a single PostgreSQL hard drive cannot hold 150 Terabytes of data efficiently. 
2. **The Conclusion:** Therefore, you look at the interviewer and say: "Because we need to store 150TB of data over 5 years, a standard relational database will hit vertical scaling limits. I propose we use a horizontally scalable NoSQL database like Cassandra or Amazon DynamoDB, which can easily distribute 150TB across dozens of physical nodes."

## Success Criteria
You have successfully completed this practice if you understand that doing basic math *before* drawing the architecture prevents you from proposing a solution that will mathematically fail in the real world.
