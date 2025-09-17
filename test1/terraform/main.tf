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
    context    = "${path.module}/.."
    dockerfile = "${path.module}/../Dockerfile"
  }
}

output "image_id" {
  value = docker_image.pypelines_image.image_id
}
