terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.21"
    }
  }
}

provider "docker" {}

resource "docker_image" "pypelines_image" {
  name         = "pypelines:latest"
  build {
    # use repo root as context from terraform module
    context    = "${path.module}/.."
    dockerfile = "${path.module}/../Dockerfile"
  }
}

output "image_id" {
  value = docker_image.pypelines_image.image_id
}

// --- GitHub provider and branch protection (optional) ---
// This section configures branch protection for `main` or `master` using the GitHub provider.
// To apply these changes, set the following environment variables/secrets for Terraform:
// - GITHUB_TOKEN (a token with admin:repo scope) or configure provider accordingly.

provider "github" {
  // token can be provided via environment variable GITHUB_TOKEN or via terraform variable
}

resource "github_branch_protection" "protect_main" {
  repository_id = data.github_repository.this.node_id
  pattern       = "main"

  required_status_checks {
    strict   = true
    contexts = ["checks"]
  }

  required_pull_request_reviews {
    dismissal_restrictions = []
    dismiss_stale_reviews   = true
    require_code_owner_reviews = false
    required_approving_review_count = 1
  }

  enforce_admins = true
}

data "github_repository" "this" {
  full_name = "${var.github_owner}/${var.github_repo}"
}
