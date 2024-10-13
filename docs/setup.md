# Setup Guide

This guide provides detailed instructions for setting up the ServiceNow MID Server Deployment project.

## Prerequisites

Ensure you have the following installed and configured:

- Python 3.8+
- AWS CLI
- Terraform 0.14+
- Docker

## Installation Steps

1. Clone the repository:
   ```
   git clone https://github.com/your-username/servicenow-mid-ecs-deployment.git
   cd servicenow-mid-ecs-deployment
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure AWS credentials:
   ```
   aws configure
   ```
   Enter your AWS Access Key ID, Secret Access Key, and default region when prompted.

4. Set up environment variables:
   Create a `.env` file in the root directory with the following content:
   ```
   AWS_PROFILE=your_aws_profile
   AWS_REGION=your_aws_region
   ENVIRONMENT=dev  # or staging, prod
   ```

5. Set up Terraform variables:
   Create a `terraform/terraform.tfvars` file with the necessary variables. Do not include sensitive information in this file. Example:
   ```
   aws_region         = "us-west-2"
   environment        = "dev"
   vpc_cidr           = "10.0.0.0/16"
   ecr_repo_url       = "YOUR_ECR_REPO_URL"
   mid_instance_url   = "https://your-instance.service-now.com"
   mid_instance_username = "mid_user"
   mid_server_name    = "mid-server-dev-01"
   ```

6. Initialize Terraform:
   ```
   cd terraform
   terraform init
   ```

7. (Optional) Set up GitHub Secrets for CI/CD:
   In your GitHub repository, go to Settings > Secrets and add the following secrets:
   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_REGION

## Next Steps

After completing the setup, refer to the [Usage Guide](usage.md) for instructions on how to deploy and manage your ServiceNow MID Server on AWS ECS.