output "cloudtrail_s3_bucket_name" {
  value = module.cloudtrail.s3_bucket_name
}

output "ecs_logs_s3_bucket_name" {
  value = module.ecs.s3_bucket_name
}

output "vpc_id" {
  value = module.vpc.vpc_id
}

output "db_host" {
  value = module.database.db_host
}

output "asg_name" {
  value = module.ecs.asg_name
}

output "ecs_service_name" {
  value = module.ecs.ecs_service_name
}

output "ecs_cluster_name" {
  value = module.ecs.ecs_cluster_name
}

output "region" {
  value = var.region
}

output "ec2_hostname" {
  value = var.ec2_hostname
}

output "ec2_public_dns_hostname" {
  value = module.ecs.ec2_public_dns_hostname
}

output "ec2_public_ip_address" {
  value = module.ecs.ec2_public_ip_address
}
