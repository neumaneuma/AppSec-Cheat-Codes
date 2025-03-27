terraform {
  backend "s3" {
    bucket       = "main-state-e58c7d60-1ee2-0cd7-f39c-ebc5fedb9351"
    key          = "state/aws.tfstate"
    region       = "us-east-1"
    use_lockfile = true
  }
}

# Default provider configuration
provider "aws" {
  region = var.region
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

# S3 bucket names must be globally unique, so we use a random UUID to generate a unique name
resource "random_uuid" "uuid" {}

data "http" "cloudflare_ips" {
  url = "https://api.cloudflare.com/client/v4/ips"
}

locals {
  cloudflare_ipv4_addresses = jsondecode(data.http.cloudflare_ips.response_body).result.ipv4_cidrs
  db_password               = var.db_password == null ? data.aws_ssm_parameter.db_password[0].value : var.db_password
}

# Get existing password from SSM only if db_password variable is not provided
data "aws_ssm_parameter" "db_password" {
  count = var.db_password == null ? 1 : 0
  name  = var.db_password_ssm_name
}

# Create/update SSM parameter (update will only occur if db_password variable is provided and is different
# from the current value)
resource "aws_ssm_parameter" "db_password" {
  name        = var.db_password_ssm_name
  description = "Database password"
  type        = "SecureString"
  value       = local.db_password
}

module "cloudtrail" {
  source      = "../modules/cloudtrail"
  region      = var.region
  trail_name  = "permissions-audit-trail"
  bucket_name = "cloudtrail-audit-logs-${random_uuid.uuid.result}"
}

module "certificates" {
  source          = "../modules/certificates"
  domain_name     = var.domain_name
  api_domain_name = var.api_domain_name
  region          = var.region
}

module "vpc" {
  source = "../modules/vpc"
  region = var.region
}

module "ecs" {
  source                                 = "../modules/ecs"
  region                                 = var.region
  rds_instance_url                       = module.database.db_host
  db_password                            = local.db_password
  bucket_name                            = "ecs-logs-${random_uuid.uuid.result}"
  public_subnet_ids                      = module.vpc.public_subnets[*].id
  private_subnet_ids                     = module.vpc.private_subnets[*].id
  public_subnet_cidr_blocks              = module.vpc.public_subnets[*].cidr_block
  private_subnet_cidr_blocks             = module.vpc.private_subnets[*].cidr_block
  docker_hub_repo                        = var.docker_hub_repo
  vpc_id                                 = module.vpc.vpc_id
  backend_cloudwatch_log_group_name      = var.backend_cloudwatch_log_group_name
  internal_api_cloudwatch_log_group_name = var.internal_api_cloudwatch_log_group_name
  ec2_hostname                           = var.ec2_hostname
  db_security_group_id                   = module.database.db_security_group_id
  cloudflare_ipv4_addresses              = local.cloudflare_ipv4_addresses
  origin_certificate                     = module.certificates.origin_certificate
  private_key_pem                        = module.certificates.private_key_pem
}

module "database" {
  source                     = "../modules/database"
  region                     = var.region
  vpc_id                     = module.vpc.vpc_id
  ecs_sg_id                  = module.ecs.ecs_sg_id
  private_subnet_ids         = module.vpc.private_subnets[*].id
  private_subnet_cidr_blocks = module.vpc.private_subnets[*].cidr_block
  db_name                    = var.db_name
  db_username                = var.db_username
  db_password                = local.db_password
}
