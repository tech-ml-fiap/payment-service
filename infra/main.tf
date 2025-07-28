terraform {
  required_version = ">= 1.6"
  required_providers {
    aws    = { source = "hashicorp/aws", version = "~> 5.0" }
    random = { source = "hashicorp/random", version = "~> 3.5" }
  }
}

provider "aws" { region = "us-east-1" }

# ------------------------------------------------------------------
# Recursos já existentes
# ------------------------------------------------------------------
data "aws_ecr_repository" "payment" { name = "payment-service" }

# Somente Amazon Linux 2 Docker
data "aws_elastic_beanstalk_solution_stack" "docker_al2_latest" {
  name_regex  = "^64bit Amazon Linux 2 v.*running Docker$"
  most_recent = true
}

# ------------------------------------------------------------------
# Recursos a criar
# ------------------------------------------------------------------
resource "random_id" "suffix" { byte_length = 4 }

resource "aws_elastic_beanstalk_application" "app" {
  name = "payment-service"
}

resource "aws_elastic_beanstalk_environment" "env" {
  name                = "payment-service-env-${random_id.suffix.hex}"
  application         = aws_elastic_beanstalk_application.app.name
  solution_stack_name = data.aws_elastic_beanstalk_solution_stack.docker_al2_latest.name
  cname_prefix        = "payment-service-${random_id.suffix.hex}"

  setting {
    namespace = "aws:elasticbeanstalk:container:docker"
    name      = "Image"
    value     = "${data.aws_ecr_repository.payment.repository_url}:latest"
  }
  setting {
    namespace = "aws:elasticbeanstalk:environment"
    name      = "ServiceRole"
    value     = "LabRole"
  }
  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = "LabInstanceProfile"
  }
}

# ------------------------------------------------------------------
# Outputs
# ------------------------------------------------------------------
output "service_url" {
  description = "URL pública do payment-service"
  value       = "http://${aws_elastic_beanstalk_environment.env.endpoint_url}"
}

output "ecr_repo_url" {
  description = "URI do repositório ECR"
  value       = data.aws_ecr_repository.payment.repository_url
}
