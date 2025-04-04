variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "domain_name" {
  description = "Domain name"
  type        = string
  default     = "ctf.neumaneuma.com"
}

variable "api_domain_name" {
  description = "API domain name"
  type        = string
  default     = "api.ctf.neumaneuma.com"
}

variable "cloudflare_api_token" {
  description = "Cloudflare API token"
  type        = string
  sensitive   = true
  default     = null # force terraform to use $CLOUDFLARE_API_TOKEN environment variable
}

variable "docker_hub_repo" {
  description = "Docker Hub repository identifier"
  type        = string
  default     = "neumaneuma/appseccheatcodes"
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
  description = "Database password - only required for initial setup (or to update the password), afterwards retrieved from SSM"
  type        = string
  sensitive   = true
  default     = null # Comment out to make the variable required
}

variable "backend_cloudwatch_log_group_name" {
  description = "Cloudwatch log group name for backend"
  type        = string
  default     = "/ecs/backend"
}

variable "internal_api_cloudwatch_log_group_name" {
  description = "Cloudwatch log group name for internal_api"
  type        = string
  default     = "/ecs/internal_api"
}

variable "ec2_hostname" {
  description = "EC2 hostname"
  type        = string
  default     = "ecs-instance"
}

variable "db_password_ssm_name" {
  description = "SSM parameter name for database password"
  type        = string
  default     = "/database/password"
}
