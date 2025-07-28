terraform {
  required_version = ">= 1.6"
  required_providers {
    aws     = { source = "hashicorp/aws", version = "~> 5.0" }
    random  = { source = "hashicorp/random", version = "~> 3.5" }
  }
}

provider "aws" { region = "us-east-1" }

########################################
# Variáveis vindas da pipeline
########################################
variable "app_version"  { type = string }
variable "artifact_zip" { type = string }

########################################
# Nome único usando Account ID
########################################
data "aws_caller_identity" "me" {}

resource "aws_s3_bucket" "artifacts" {
  bucket        = "payment-service-artifacts-${data.aws_caller_identity.me.account_id}"
  force_destroy = true
}

resource "aws_s3_object" "pkg" {
  bucket = aws_s3_bucket.artifacts.id
  key    = "build-${var.app_version}.zip"
  source = var.artifact_zip
  etag   = filemd5(var.artifact_zip)
}

########################################
# Elastic Beanstalk (sem OptionSetting Image)
########################################
resource "aws_elastic_beanstalk_application" "app" {
  name = "payment-service"
}

resource "aws_elastic_beanstalk_application_version" "ver" {
  name        = var.app_version
  application = aws_elastic_beanstalk_application.app.name
  bucket      = aws_s3_bucket.artifacts.id
  key         = aws_s3_object.pkg.key
}

data "aws_elastic_beanstalk_solution_stack" "docker_al2_latest" {
  name_regex  = "^64bit Amazon Linux 2 v.*running Docker$"
  most_recent = true
}

resource "random_id" "suffix" { byte_length = 4 }

resource "aws_elastic_beanstalk_environment" "env" {
  name                = "payment-service-env-${random_id.suffix.hex}"
  application         = aws_elastic_beanstalk_application.app.name
  solution_stack_name = data.aws_elastic_beanstalk_solution_stack.docker_al2_latest.name
  version_label       = aws_elastic_beanstalk_application_version.ver.name
  cname_prefix        = "payment-service-${random_id.suffix.hex}"

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

output "service_url" {
  value       = "http://${aws_elastic_beanstalk_environment.env.endpoint_url}"
  description = "Endpoint público"
}
