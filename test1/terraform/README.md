# Terraform: build Docker image

This folder contains a minimal Terraform configuration that builds the Docker image using the local Docker provider.

Steps:

```bash
cd terraform
terraform init
terraform apply -auto-approve
```

This will build the image using the `Dockerfile` in the project root and output the image id.
