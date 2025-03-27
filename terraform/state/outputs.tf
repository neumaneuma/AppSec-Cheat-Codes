output "main_state_bucket_name" {
  value = aws_s3_bucket.main_state.id
}

output "iam_state_bucket_name" {
  value = aws_s3_bucket.iam_state.id
}
