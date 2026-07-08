# Practice Guide: Chapter 20 (Volume 3)

## Objective
To install the Redis server and use the command-line interface to interact with a Key-Value store.

## Assignment 1: Installation
We need to install the Redis daemon and the `redis-cli` tool.

1. Install the packages:
   * **Ubuntu/Debian:** `sudo apt update && sudo apt install redis-server`
   * **RHEL/CentOS:** `sudo dnf install redis`
2. Start the service:
   `sudo systemctl start redis` (RHEL might require `redis-server`)
3. Open the interactive command-line interface:
   `redis-cli`
4. **Observation:** Your terminal prompt will change to `127.0.0.1:6379>`. You are now talking directly to the RAM cache!

## Assignment 2: The Key-Value Store
Let's manually cache a piece of theoretical database data.

1. Let's pretend the database just took 10 seconds to calculate the total number of users. Save that number into the cache:
   `SET total_users 14500`
2. **Observation:** Redis will respond with `OK`.
3. Now, pretend you are a web application loading the homepage. Fetch the number:
   `GET total_users`
4. **Result:** Redis instantly returns `"14500"`.

## Assignment 3: Expiration (TTL)
We don't want to store this number forever, because new users might sign up! Let's set it to expire in 10 seconds.

1. Overwrite the key, but add the `EX` flag (for expire) followed by 10 seconds:
   `SET total_users 14500 EX 10`
2. Quickly fetch the key to prove it is there:
   `GET total_users`
3. Wait for 11 seconds.
4. Fetch the key again:
   `GET total_users`
5. **Observation:** Redis returns `(nil)`. The TTL expired, and Redis automatically purged the data from memory to make room for new data! The application must now go ask MySQL for the fresh number.

## Assignment 4: Cleanup
1. Exit the Redis interface:
   `exit`

## Success Criteria
You have successfully completed this practice if you installed the Redis server, used `redis-cli` to `SET` and `GET` a key, and successfully utilized the `EX` flag to watch a cached item expire and disappear.
