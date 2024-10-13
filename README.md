# ServiceNow MID Server Deployment on AWS ECS

This project automates the deployment of ServiceNow MID (Management, Instrumentation, and Discovery) Servers on AWS Elastic Container Service (ECS) using Python and Terraform.

## Features

- Automated deployment of ServiceNow MID Servers on AWS ECS
- Infrastructure as Code using Terraform
- CI/CD pipeline using GitHub Actions
- Secure parameter management using AWS Systems Manager Parameter Store
- Docker container management for MID Server instances

## Prerequisites

- Python 3.8+
- AWS CLI configured with appropriate permissions
- Terraform 0.14+
- Docker

## Quick Start

1. Clone the repository:
   ```
   git clone https://github.com/your-username/servicenow-mid-ecs-deployment.git
   cd servicenow-mid-ecs-deployment
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up AWS credentials:
   ```
   aws configure
   ```

4. Initialize Terraform:
   ```
   cd terraform
   terraform init
   ```

5. Deploy the MID Server:
   ```
   python src/scripts/deploy.py
   ```

## Documentation

For detailed setup and usage instructions, please refer to the following documents:

- [Setup Guide](docs/setup.md)
- [Usage Guide](docs/usage.md)

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.