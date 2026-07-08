# Practice Guide: Chapter 6 (Volume 3)

## Objective
To familiarize yourself with reading and writing basic SQL statements before we install the actual database software in the next chapter.

## Assignment 1: The ERD (Entity Relationship Diagram)
Imagine you are building a database for a small bookstore. You have two tables: `books` and `authors`. 

1. Create a text file called `bookstore_schema.txt`:
   `nano ~/bookstore_schema.txt`
2. Sketch out the schema (the columns) for the `authors` table. 
   *(Hint: It needs a Primary Key, a First Name, and a Last Name).*
3. Sketch out the schema for the `books` table.
   *(Hint: It needs a Primary Key, a Title, a Price, and an `author_id` to link it to the authors table).*
4. Save your sketch and exit.

## Assignment 2: Writing SQL Statements
Now, write the theoretical SQL commands to interact with the database you just designed. Add these to your text file.

1. Write the SQL statement to insert a new author named "Stephen King".
   `INSERT INTO ...`
2. Write the SQL statement to insert a new book called "The Shining" for $19.99.
3. Write the SQL statement to fetch all books that cost more than $15.00.
   `SELECT ... FROM ... WHERE ...`

## Assignment 3: Testing Ports
Let's practice the network troubleshooting scenario from the chapter. 

1. Attempt to connect to a theoretical MySQL database running on Google's DNS server using `nc` (netcat):
   `nc -vz 8.8.8.8 3306`
2. **Observation:** The connection will hang or time out. Why? Because Google's DNS server does not run MySQL, and their firewall is actively dropping your packets on Port 3306! Press `Ctrl+C` to cancel.
3. Now attempt to connect to Port 443 (HTTPS) on Google:
   `nc -vz google.com 443`
4. **Observation:** It will instantly say `Connection to google.com 443 port [tcp/https] succeeded!`. The port is open!

## Success Criteria
You have successfully completed this practice if you conceptually designed a relational database schema, wrote basic SQL syntax, and used `netcat` (`nc`) to prove whether a specific network port was open or blocked.
