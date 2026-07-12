# Practice Guide: Chapter 24 (Volume 3)

## Objective
To prove container ephemerality by writing data, destroying a container, and recovering the data using a Named Volume.

## Assignment 1: The Ephemeral Disaster
First, let's watch data disappear forever. 

1. Run an interactive Ubuntu container:
   `sudo docker run -it --name disaster ubuntu bash`
2. Create a very important file inside the container:
   `echo "SUPER SECRET DATA" > /important.txt`
3. Exit the container:
   `exit`
4. The container is now stopped. Let's delete it completely (which is what happens during an image upgrade):
   `sudo docker rm disaster`
5. Try to find your important data. You can't. It is gone forever. 

## Assignment 2: The Named Volume Solution
Let's do it the correct way. We will attach a Named Volume.

1. Tell Docker to create a Named Volume called `safe_data`:
   `sudo docker volume create safe_data`
2. Run a new Ubuntu container, but this time, mount (`-v`) the `safe_data` volume to the `/data` folder inside the container:
   `sudo docker run -it --name safe_box -v safe_data:/data ubuntu bash`
3. Notice you are inside the container. Create a very important file, but make sure to put it inside the `/data` folder!
   `echo "THIS DATA WILL SURVIVE" > /data/important.txt`
4. Exit the container:
   `exit`
5. Destroy the container completely:
   `sudo docker rm safe_box`

## Assignment 3: The Resurrection
The container is dead. But what about the Volume?

1. Let's spin up a brand new, completely different container (we will use Alpine this time). Attach the exact same Volume to it!
   `sudo docker run -it --name new_box -v safe_data:/data alpine sh`
2. Check the `/data` folder inside this new container:
   `cat /data/important.txt`
3. **Result:** It prints `THIS DATA WILL SURVIVE`! The data outlived the container that created it! 

## Assignment 4: Cleanup
1. Exit the new container and destroy it:
   `exit`
   `sudo docker rm new_box`
2. The Volume still exists on your hard drive! To clean up the host OS and delete the Volume, run:
   `sudo docker volume rm safe_data`

## Success Criteria
You have successfully completed this practice if you destroyed an ephemeral container causing data loss, and then successfully used `-v safe_data:/data` to write data to a volume that survived the deletion of its host container.
