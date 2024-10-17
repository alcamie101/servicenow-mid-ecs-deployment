# ServiceNow MID Server Deployment on AWS ECS

This project automates the deployment of ServiceNow MID (Management, Instrumentation, and Discovery) Servers on AWS Elastic Container Service (ECS) using Python and Terraform.

## Features

- Automated deployment of ServiceNow MID Servers on AWS ECS
- Infrastructure as Code using Terraform
- CI/CD pipeline using GitHub Actions
- Secure parameter management using AWS Systems Manager Parameter Store
- Docker container management for MID Server instances

## Prerequisites

- Python 3.12+
- AWS CLI configured with appropriate permissions
- Terraform 1.9.5+
- Docker 27.2+

## Project Structure

```
servicenow-mid-ecs-deployment/
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── config
│   └── example.env
├── docker
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs
│   ├── setup.md
│   └── usage.md
├── requirements.txt
├── setup.py
├── src
│   ├── __init__.py
│   ├── aws_utils
│   │   ├── __init__.py
│   │   ├── ec2.py
│   │   ├── ecs.py
│   │   ├── iam.py
│   │   └── ssm.py
│   ├── config.py
│   ├── deployment
│   │   ├── __init__.py
│   │   ├── mid_server.py
│   │   └── parameter_store.py
│   └── scripts
│       ├── build.py
│       ├── deploy.py
│       ├── rollback.py
│       └── setup_params.py
├── terraform
│   ├── dev.tfvars
│   ├── ecs.tf
│   ├── main.tf
│   ├── outputs.tf
│   ├── prod.tfvars
│   ├── stage.tfvars
│   ├── terraform.tfvars
│   └── variables.tf
└── tests
    ├── integration
    │   ├── test_deployment_process.py
    │   └── test_mid_server_deployer.py
    └── unit
        ├── test_aws_utils.py
        ├── test_deployment.py
        ├── test_ec2_utils.py
        ├── test_ecs_utils.py
        ├── test_iam_utils.py
        └── test_ssm_utils.py
```

## Quick Start

1. Clone the repository:
   ```
   git clone https://github.com/alcamie101/servicenow-mid-ecs-deployment.git
   cd servicenow-mid-ecs-deployment
   ```

2. Set up a virtual environment and install dependencies:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
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

## Running Tests

To run unit tests:
```
python -m unittest discover tests/unit
```

To run integration tests:
```
python -m unittest discover tests/integration
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.