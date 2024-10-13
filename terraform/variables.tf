variable "aws_region" {
  description = "The AWS region to deploy to"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "The environment (dev, staging, prod)"
  type        = string
}

variable "vpc_cidr" {
  description = "The CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "ecr_repo_url" {
  description = "The URL of the ECR repository"
  type        = string
}

variable "mid_instance_url" {
  description = "The URL of the ServiceNow instance"
  type        = string
}

variable "mid_instance_username" {
  description = "The username for the ServiceNow instance"
  type        = string
}

variable "mid_instance_password" {
  description = "The password for the ServiceNow instance"
  type        = string
  sensitive   = true
}

variable "mid_server_name" {
  description = "The name of the MID server"
  type        = string
}