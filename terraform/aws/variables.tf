variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "domain_name" {
  description = "Domain name"
  type        = string
  default     = "appseccheat.codes"
}

variable "cloudflare_api_token" {
  description = "Cloudflare API token"
  type        = string
  default     = null # force terraform to use $CLOUDFLARE_API_TOKEN environment variable
  sensitive   = true
}

variable "traffic_distribution" {
  description = "Levels of traffic distribution"
  type        = string
  default     = "blue"
}

variable "docker_hub_repo" {
  description = "Docker Hub repository identifier"
  type        = string
  default     = "neumaneuma/appseccheat.codes"
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "postgres"
}

variable "db_username" {
  description = "Database username"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
  default     = "dbesrdgtfhjklgdmrfseadjfbcgofdklmsea" # putting here until development is complete for ease of development
}

variable "iam_user_name" {
  description = "IAM user name"
  type        = string
  default     = "iam_user" # hardcoded to match the terraform/iam/main.tf file
}
