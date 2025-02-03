terraform {
  backend "s3" {
    bucket         = "main-state-e58c7d60-1ee2-0cd7-f39c-ebc5fedb9351"
    key            = "state/cloudflare.tfstate"
    region         = "us-east-1"
    dynamodb_table = "main-state-locks"
  }
}

provider "cloudflare" {}


data "terraform_remote_state" "aws" {
  backend = "s3"
  config = {
    bucket = "main-state-e58c7d60-1ee2-0cd7-f39c-ebc5fedb9351"
    key    = "state/aws.tfstate"
    region = var.region
  }
}

data "cloudflare_zone" "domain" {
  # TODO cloudflare has a bug so this doesn't work yet
  filter = {
    name = var.domain_name
  }
}

resource "cloudflare_dns_record" "backend" {
  zone_id = data.cloudflare_zone.domain.zone_id
  name    = var.api_domain_name
  content = data.terraform_remote_state.aws.outputs.ec2_public_ip_address
  type    = "A"
  proxied = true
  ttl     = 1
}
