# Terraform for pypelines

This folder contains Terraform configuration used during development to build the Docker image and optionally manage repository settings such as branch protection for `main`.

WARNING: Applying the branch protection resource will modify repository settings and requires a token with administrative permissions. Test in a sandbox repository first.

Prerequisites
- Terraform 1.0+
- A GitHub token with admin:repo scope available as an environment variable `GITHUB_TOKEN` (or configure the provider as you prefer).
- Copy `terraform.tfvars.example` to `terraform.tfvars` and fill in `github_owner` and `github_repo`.

Quick start

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# edit terraform.tfvars to confirm github_owner/github_repo
export GITHUB_TOKEN=ghp_...   # token with admin:repo scope
terraform init
terraform apply
```

What this does
- Builds a Docker image using the repository root as context (same as the CI build). The built image ID is output as `image_id`.
- Optionally applies branch protection rules to the `main` branch (if provider token is configured and variables point to this repo).

Security notes
- Do not store admin tokens in source control. Use GitHub Actions + a GitHub App or deploy-time secrets for automation in CI.
# Terraform: build Docker image

This folder contains a minimal Terraform configuration that builds the Docker image using the local Docker provider.

Steps:

```bash
cd terraform
terraform init
terraform apply -auto-approve
```

This will build the image using the `Dockerfile` in the project root and output the image id.
