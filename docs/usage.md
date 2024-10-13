# Usage Guide

This guide provides instructions on how to use the ServiceNow MID Server Deployment project.

## Deploying the MID Server

To deploy the MID server, run the following command from the root directory of the project:

```
python src/scripts/deploy.py --env [environment]
```

Replace `[environment]` with either `dev`, `staging`, or `prod`.

Example:
```
python src/scripts/deploy.py --env dev
```

This will:
1. Set up the necessary AWS infrastructure using Terraform
2. Deploy the MID server container to AWS ECS
3. Configure the MID server with the provided ServiceNow instance details

## Monitoring the Deployment

You can monitor the deployment process in several ways:

1. Check the console output for logs and any error messages.
2. Log into the AWS Management Console and navigate to the ECS service to view the task status.
3. Check CloudWatch logs for detailed container logs.

## Updating the MID Server

To update the MID server (e.g., with a new Docker image or configuration):

1. Update the necessary files (e.g., Terraform configurations, Docker image)
2. Run the deployment script again:
   ```
   python src/scripts/deploy.py --env [environment]
   ```

The script will detect changes and update the existing deployment.

## Running Tests

To run the unit tests:

```
python -m unittest discover tests/unit
```

To run integration tests:

```
python -m unittest discover tests/integration
```

## Troubleshooting

If you encounter issues during deployment:

1. Check the console output for error messages.
2. Verify your AWS credentials and permissions.
3. Check the CloudWatch logs for the ECS tasks.
4. Ensure all required environment variables and Terraform variables are set correctly.

For persistent issues, please open an issue in the GitHub repository with details about the problem and any relevant log outputs.

## CI/CD Pipeline

The project includes a CI/CD pipeline configured with GitHub Actions. On every push to the main branch:

1. Tests are run automatically.
2. If tests pass, the MID server is deployed to the development environment.

Ensure that you've set up the necessary GitHub Secrets for this to work correctly.

## Manual Terraform Operations

If you need to manually apply Terraform changes:

1. Navigate to the Terraform directory:
   ```
   cd terraform
   ```

2. Plan the changes:
   ```
   terraform plan
   ```

3. Apply the changes:
   ```
   terraform apply
   ```

Remember to be cautious when manually applying Terraform changes, as this can affect your running infrastructure.