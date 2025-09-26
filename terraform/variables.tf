variable "image_name" {
  description = "Name for the built Docker image"
  type        = string
  default     = "pypelines:latest"
}

variable "github_owner" {
  description = "GitHub owner/org name for repository"
  type        = string
}

variable "github_repo" {
  description = "Repository name for setting branch protection (e.g. pypelines)"
  type        = string
}
