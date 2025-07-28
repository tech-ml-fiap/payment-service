terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" {
  region = "us-east-1"
}

# ----- ECR -------------------------------------------------------
resource "aws_ecr_repository" "payment" {
  name                 = "payment-service"
  image_tag_mutability = "MUTABLE"
}

# ----- Elastic Beanstalk ----------------------------------------
resource "aws_elastic_beanstalk_application" "app" {
  name = "payment-service"
}

resource "aws_elastic_beanstalk_environment" "env" {
  name                = "payment-service-env"
  application         = aws_elastic_beanstalk_application.app.name
  solution_stack_name = "64bit Amazon Linux 2 v3.8.5 running Docker"
  cname_prefix        = "payment-service-${random_id.suffix.hex}"

  setting {
    namespace = "aws:elasticbeanstalk:container:docker"
    name      = "Image"
    value     = "${aws_ecr_repository.payment.repository_url}:latest"
  }

  # reaproveita as permissões que já existem na conta Academy
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

resource "random_id" "suffix" {
  byte_length = 4
}

output "service_url" {
  value       = "http://${aws_elastic_beanstalk_environment.env.endpoint_url}"
  description = "URL pública do payment-service"
}
