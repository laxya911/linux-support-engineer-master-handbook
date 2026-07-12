# Practice Guide: Chapter 13 (Volume 4)

## Objective
To download the HashiCorp Vault CLI, start a local development server, and read/write secrets using the Key-Value (KV) engine.

## Assignment 1: Installation and Startup
Vault is a single binary executable written in Go, just like Terraform!

1. Download the latest binary for Linux:
   `curl -LO "https://releases.hashicorp.com/vault/1.15.1/vault_1.15.1_linux_amd64.zip"`

2. Unzip it and move it to your PATH:
   `unzip vault_1.15.1_linux_amd64.zip`
   `sudo mv vault /usr/local/bin/`

3. Verify the installation:
   `vault --version`
4. Start a local, in-memory development server (This will occupy your terminal, so open a second terminal tab for the next steps!):
   `vault server -dev`

## Assignment 2: Authentication
Look at the output in the terminal where you started the server. It will provide you with an `export VAULT_ADDR` command and a `Root Token`. 

1. In your **second** terminal tab, tell the Vault CLI where the server is running:
   `export VAULT_ADDR='http://127.0.0.1:8200'`

2. Authenticate to the server using the Root Token provided in the first terminal:
   `vault login <PASTE_YOUR_ROOT_TOKEN_HERE>`

3. **Observation:** You are now authenticated as the root administrator of the Vault server.

## Assignment 3: The Key-Value (KV) Engine
The Dev server automatically enables a KV engine at the path `secret/`. This acts exactly like a secure, encrypted folder structure.

1. Write a static secret into Vault at the path `secret/myapp/database`:
   `vault kv put secret/myapp/database password="SuperSecurePassword123" username="dbadmin"`

2. **Observation:** Vault confirms the data was written. The data is now encrypted in memory!

3. Now, pretend you are an application starting up. Retrieve the secret:
   `vault kv get secret/myapp/database`
4. **Result:** Vault decrypts the data and returns the username and password to your terminal.

## Assignment 4: Cleanup

1. Because this was a `-dev` server, everything is stored in RAM. Simply go back to your first terminal tab and press `Ctrl+C`. The server will shut down, and the secrets will be permanently destroyed. 

## Success Criteria
You have successfully completed this practice if you started a local Vault server, authenticated with a Root Token, and successfully wrote and read a static secret from the Key-Value engine.
