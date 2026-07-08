# Practice Guide: Chapter 21 (Volume 3)

## Objective
To install the Docker Engine and prove that a container runs in total isolation from your host Virtual Machine.

## Assignment 1: Installation
We must install the Docker Engine on your VM.

1. **Ubuntu:**
   `sudo apt update`
   `sudo apt install docker.io`
2. **RHEL/CentOS:**
   *(RHEL natively uses Podman, which is identical to Docker. Install it via:)*
   `sudo dnf install podman podman-docker`
3. Verify the installation by checking the version:
   `docker --version`

## Assignment 2: The Hello World
Let's ask Docker to download an image from the internet (Docker Hub) and run it.

1. Run the official test image:
   `sudo docker run hello-world`
2. **Observation:** Docker will state `Unable to find image locally`. It will reach out to Docker Hub, download the tiny image, and run it. You will see a welcome message proving your engine is working!

## Assignment 3: Proving Isolation
If you are running an Ubuntu VM, you might think running an Ubuntu container is redundant. Let's prove it is a completely different environment.

1. First, check your host VM's OS release:
   `cat /etc/os-release`
   *(Take note of the specific version, e.g., Ubuntu 26.04 or RHEL 10).*
2. Now, tell Docker to download an entirely different OS image (Alpine Linux) and drop you into an interactive terminal inside the container (`-it`):
   `sudo docker run -it alpine /bin/sh`
3. **Observation:** Your terminal prompt just changed! You are now "inside" the container!
4. Check the OS release *inside* the container:
   `cat /etc/os-release`
5. **Result:** It says Alpine Linux! You are running an Alpine Linux environment *on top* of your Ubuntu/RHEL kernel. 
6. Create a file inside the container:
   `touch /hello-from-the-container.txt`
7. Exit the container:
   `exit`
8. Search for that file on your host VM:
   `ls /hello-from-the-container.txt`
9. **Result:** `No such file or directory`. The container's filesystem was completely isolated!

## Success Criteria
You have successfully completed this practice if you installed Docker, ran an Alpine container interactively, proved the OS was different from your host, and proved the filesystem was isolated.
