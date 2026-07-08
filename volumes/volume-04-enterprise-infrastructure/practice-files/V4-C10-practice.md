# Practice Guide: Chapter 10 (Volume 4)

## Objective
To conceptually design a `.gitlab-ci.yml` pipeline that lints Terraform code and deploys it to a staging environment.

## Assignment 1: The Pipeline Structure
GitLab CI (like GitHub Actions) uses a YAML file placed in the root of your repository to define the pipeline.

1. Open a blank text file:
   `nano .gitlab-ci.yml`
2. First, we define the "stages" of our pipeline. These run sequentially. If a stage fails, the pipeline stops.
   ```yaml
   stages:
     - validate
     - plan
     - deploy
   ```

## Assignment 2: The CI Phase (Validation)
The first stage is Continuous Integration. We want to test the code before we try to deploy it.

1. Add the `validate` job to your YAML file. We instruct the runner to use a Docker image that already has Terraform installed:
   ```yaml
   terraform-validate:
     stage: validate
     image: hashicorp/terraform:latest
     script:
       - terraform init -backend=false
       - terraform validate
       - terraform fmt -check
   ```
2. **Analysis:** If a developer makes a syntax error, `terraform validate` will exit with a non-zero code. The CI runner will detect this, mark the pipeline as "Failed" (Red), and prevent the code from being deployed.

## Assignment 3: The CD Phase (Deployment)
If the code is valid, we move to Continuous Deployment.

1. Add the `plan` and `deploy` jobs to your YAML file:
   ```yaml
   terraform-plan:
     stage: plan
     image: hashicorp/terraform:latest
     script:
       - terraform init
       - terraform plan -out=tfplan
     artifacts:
       paths:
         - tfplan

   terraform-deploy:
     stage: deploy
     image: hashicorp/terraform:latest
     script:
       - terraform init
       - terraform apply -auto-approve tfplan
     only:
       - main
   ```
2. **Analysis:** The `deploy` job has a special rule: `only: - main`. This guarantees that if a developer pushes code to a `feature-branch`, the pipeline will validate it, but it will *never* attempt to deploy it to production! It will only deploy if the code is merged into the `main` branch.

3. Save and close your file.

## Success Criteria
You have successfully completed this practice if you conceptually understand how a pipeline file instructs an ephemeral runner to execute a sequence of commands, and how constraints (like `only: main`) protect the production environment from unreviewed code.
