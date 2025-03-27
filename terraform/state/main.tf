provider "aws" {
  region = var.region
}

resource "random_uuid" "uuid" {
}

resource "aws_s3_bucket" "main_state" {
  bucket = "main-state-${random_uuid.uuid.result}" # Must be globally unique
}

resource "aws_s3_bucket_versioning" "main_state" {
  bucket = aws_s3_bucket.main_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "main_state" {
  bucket = aws_s3_bucket.main_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "main_state" {
  bucket = aws_s3_bucket.main_state.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket" "iam_state" {
  bucket = "iam-state-${random_uuid.uuid.result}"
}

resource "aws_s3_bucket_versioning" "iam_state" {
  bucket = aws_s3_bucket.iam_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "iam_state" {
  bucket = aws_s3_bucket.iam_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "iam_state" {
  bucket = aws_s3_bucket.iam_state.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
