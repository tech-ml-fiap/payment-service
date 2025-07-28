terraform {
  required_version = ">= 1.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

provider "aws" {
  region = "us-east-1"            # região liberada na conta Academy
}

# ------------------------------------------------------------------
# Repositório ECR já existente (somente leitura)
# ------------------------------------------------------------------
data "aws_ecr_repository" "payment" {
  name = "payment-service"
}

# ------------------------------------------------------------------
# Sufixo aleatório para evitar colisão de CNAME no Elastic Beanstalk
# ------------------------------------------------------------------
resource "random_id" "suffix" {
  byte_length = 4
}

# ------------------------------------------------------------------
# Aplicação Elastic Beanstalk
# ------------------------------------------------------------------
resource "aws_elastic_beanstalk_application" "app" {
  name = "payment-service"
}

# ------------------------------------------------------------------
# Ambiente Elastic Beanstalk
# ------------------------------------------------------------------
resource "aws_elastic_beanstalk_environment" "env" {
  name                = "payment-service-env"
  application         = aws_elastic_beanstalk_application.app.name
  solution_stack_name = "64bit Amazon Linux 2 v3.8.5 running Docker"

  # prefixo do CNAME (fica algo como payment-service-<hex>.us-east-1.elasticbeanstalk.com)
  cname_prefix = "payment-service-${random_id.suffix.hex}"

  # imagem Docker publicada no ECR
  setting {
    namespace = "aws:elasticbeanstalk:container:docker"
    name      = "Image"
    value     = "${data.aws_ecr_repository.payment.repository_url}:latest"
  }

  # papéis já existentes na conta Academy
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
# Saídas
# ------------------------------------------------------------------
output "service_url" {
  description = "URL pública do payment-service"
  value       = "http://${aws_elastic_beanstalk_environment.env.endpoint_url}"
}

output "ecr_repo_url" {
  description = "URI do repositório ECR para o push da imagem"
  value       = data.aws_ecr_repository.payment.repository_url
}
