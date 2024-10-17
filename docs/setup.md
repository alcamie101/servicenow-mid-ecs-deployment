# Setup Guide

This guide provides detailed instructions for setting up the ServiceNow MID Server Deployment project.

## Prerequisites

Ensure you have the following installed and configured:

- Python 3.12+
- AWS CLI configured with appropriate permissions
- Terraform 1.9.5+
- Docker 27.2+

## Installation Steps

1. Clone the repository:
   ```
   git clone https://github.com/alcamie101/servicenow-mid-ecs-deployment.git
   cd servicenow-mid-ecs-deployment
   ```

2. Set up a virtual environment and install dependencies:

   ### For Mac and Linux:
   ```bash
   # Create a virtual environment
   python3 -m venv venv

   # Activate the virtual environment
   source venv/bin/activate

   # Install the requirements
   pip install -r requirements.txt
   ```

   ### For Windows:
   ```cmd
   # Create a virtual environment
   python -m venv venv

   # Activate the virtual environment
   venv\Scripts\activate

   # Install the requirements
   pip install -r requirements.txt
   ```

   Note: After you're done working on the project, you can deactivate the virtual environment by running `deactivate`.

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
   aws_region         = "us-east-1"
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

## Setting up GitHub Actions for CI/CD

1. In your GitHub repository, go to the "Actions" tab.

2. GitHub should automatically detect the workflow files in the `.github/workflows` directory. If not, you can manually set up the workflows:
   - Click on "New workflow"
   - Choose "set up a workflow yourself"
   - Copy the contents of `ci.yml` and `cd.yml` into separate files

3. Set up the following secrets in your GitHub repository (Settings > Secrets):
   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - Any other environment-specific secrets (e.g., MID_INSTANCE_PASSWORD)

4. Commit and push your changes. The CI workflow will run on every push and pull request to the main and develop branches. The CD workflow will run on pushes to the main branch.

5. Monitor the Actions tab in your GitHub repository to see the workflow runs and their status.

## Troubleshooting

If you encounter issues with the virtual environment:

### For Mac and Linux:
- Ensure you have the `python3-venv` package installed. On Ubuntu or Debian, you can install it with:
  ```
  sudo apt-get install python3-venv
  ```

### For Windows:
- Make sure you have the latest version of Python installed and that it's added to your PATH.
- If you're using PowerShell and encounter permission issues, you may need to change the execution policy:
  ```
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

If you face any issues with package installation, try upgrading pip:
```
pip install --upgrade pip
```

Then attempt to install the requirements again.

## Next Steps

After completing the setup, refer to the [Usage Guide](usage.md) for instructions on how to deploy and manage your ServiceNow MID Server on AWS ECS.

Remember to activate your virtual environment (with `source venv/bin/activate` on Mac/Linux or `venv\Scripts\activate` on Windows) every time you work on this project.