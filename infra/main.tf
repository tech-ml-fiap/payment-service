terraform {
  required_version = ">= 1.6"
  required_providers {
    aws    = { source = "hashicorp/aws", version = "~> 5.0" }
    random = { source = "hashicorp/random", version = "~> 3.5" }
    archive = { source = "hashicorp/archive", version = "~> 2.4" }
  }
}

provider "aws" { region = "us-east-1" }

########################################
# Variáveis que vêm da pipeline
########################################
variable "docker_image"   { type = string }
variable "app_version"    { type = string }   # ex.: commit SHA

########################################
# Bucket de artefatos (cria 1×, importa depois)
########################################
resource "aws_s3_bucket" "artifacts" {
  bucket = "payment-service-artifacts"
  force_destroy = true
}

########################################
# Dockerrun gerado pela pipeline
########################################
data "archive_file" "zip" {
  type        = "zip"
  source_file = "${path.module}/deploy.zip"         # criado no CI
  output_path = "${path.module}/build-${var.app_version}.zip"
}

resource "aws_s3_object" "package" {
  bucket = aws_s3_bucket.artifacts.id
  key    = "build-${var.app_version}.zip"
  source = data.archive_file.zip.output_path
  etag   = filemd5(data.archive_file.zip.output_path)
}

########################################
# Beanstalk
########################################
resource "aws_elastic_beanstalk_application" "app" {
  name = "payment-service"
}

resource "aws_elastic_beanstalk_application_version" "ver" {
  name        = var.app_version
  application = aws_elastic_beanstalk_application.app.name
  bucket      = aws_s3_bucket.artifacts.id
  key         = aws_s3_object.package.key
}

resource "random_id" "suffix" { byte_length = 4 }

data "aws_elastic_beanstalk_solution_stack" "docker_al2" {
  name_regex  = "^64bit Amazon Linux 2 v.*running Docker$"
  most_recent = true
}

resource "aws_elastic_beanstalk_environment" "env" {
  name                = "payment-service-env-${random_id.suffix.hex}"
  application         = aws_elastic_beanstalk_application.app.name
  solution_stack_name = data.aws_elastic_beanstalk_solution_stack.docker_al2.name
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

########################################
# Outputs
########################################
output "service_url" {
  description = "Endpoint público da API"
  value       = "http://${aws_elastic_beanstalk_environment.env.endpoint_url}"
}
