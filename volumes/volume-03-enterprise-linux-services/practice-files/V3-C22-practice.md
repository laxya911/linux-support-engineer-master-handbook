# Practice Guide: Chapter 22 (Volume 3)

## Objective
To write a `Dockerfile`, build a custom image, and run a container that serves a custom HTML webpage.

## Assignment 1: The Code
First, we need something to put *inside* the container.

1. Create a new directory for this project and move inside it:
   `mkdir ~/my-docker-site && cd ~/my-docker-site`
2. Create a basic HTML file:
   `nano index.html`
3. Paste the following:
   ```html
   <h1>Hello from inside a Docker Container!</h1>
   ```
4. Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

## Assignment 2: The Blueprint (Dockerfile)
Now we tell Docker how to package this.

1. Create a file named exactly `Dockerfile` (Capital D, no extension):
   `nano Dockerfile`
2. We want to use NGINX. Paste the following blueprint:
   ```dockerfile
   # Step 1: Start with the official NGINX image
   FROM nginx:latest

   # Step 2: Copy our custom HTML file into the container's webroot
   COPY index.html /usr/share/nginx/html/index.html

   # Step 3: (Optional but good practice) State which port this exposes
   EXPOSE 80
   ```
3. Save and exit. 
*(Note: We didn't include a `CMD` because the base `nginx:latest` image already has a `CMD` that starts NGINX for us!)*

## Assignment 3: The Build
Let's build the image!

1. Tell Docker to build an image using the current directory (`.`) and tag (`-t`) it with the name `my-site`:
   `sudo docker build -t my-site .`
2. **Observation:** You will see Docker downloading the NGINX base image, and then executing your `COPY` step.
3. Verify the image exists on your hard drive:
   `sudo docker images`

## Assignment 4: The Execution
The image is just a blueprint. Let's run it!

1. Run the container in detached mode (`-d`) and map Port 8080 on your VM to Port 80 inside the container (`-p 8080:80`):
   `sudo docker run -d -p 8080:80 my-site`
2. Verify it is running:
   `sudo docker ps`
3. Test it! Use `curl` to hit Port 8080 on your local VM:
   `curl http://localhost:8080`
4. **Result:** You will see `<h1>Hello from inside a Docker Container!</h1>`!

## Success Criteria
You have successfully completed this practice if you wrote a `Dockerfile`, used `docker build` to create an image, and used `docker run` to execute a container that served your custom HTML file.
