import os
import json
import logging
from typing import Dict, Any, List, Optional
from ..aws_utils.ec2 import EC2Utils
from ..aws_utils.ecs import ECSUtils
from ..aws_utils.iam import IAMUtils
from ..aws_utils.ssm import SSMUtils

class MIDServerDeployer:
    def __init__(self, profile_name: str, environment: str):
        self.profile_name = profile_name
        self.environment = environment
        self.ec2_utils = EC2Utils(profile_name)
        self.ecs_utils = ECSUtils(profile_name)
        self.iam_utils = IAMUtils(profile_name)
        self.ssm_utils = SSMUtils(profile_name)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def deploy(self):
        """
        Main method to deploy the MID server.
        """
        self.logger.info(f"Starting MID server deployment for environment: {self.environment}")

        try:
            # Step 1: Create or get existing VPC and security group
            vpc_id, subnet_ids = self._setup_network()
            sg_id = self._setup_security_group(vpc_id)

            # Step 2: Create or get existing IAM roles
            task_role_arn, execution_role_arn = self._setup_iam_roles()

            # Step 3: Create or get existing ECS cluster
            cluster_name = self._setup_ecs_cluster()

            # Step 4: Register task definition
            task_definition_arn = self._register_task_definition(task_role_arn, execution_role_arn)

            # Step 5: Create or update ECS service
            self._setup_ecs_service(cluster_name, task_definition_arn, subnet_ids, [sg_id])

            self.logger.info(f"MID server deployment completed for environment: {self.environment}")
        except Exception as e:
            self.logger.error(f"Error during MID server deployment: {str(e)}")
            raise

    def _setup_network(self) -> tuple:
        """Set up VPC and subnets."""
        try:
            vpcs = self.ec2_utils.describe_vpcs()
            if not vpcs['Vpcs']:
                self.logger.error("No VPCs found. Please create a VPC before deploying.")
                raise ValueError("No VPCs found")
            
            vpc_id = vpcs['Vpcs'][0]['VpcId']
            subnets = self.ec2_utils.describe_subnets(vpc_id)
            subnet_ids = [subnet['SubnetId'] for subnet in subnets['Subnets']]
            
            self.logger.info(f"Using VPC: {vpc_id} with subnets: {', '.join(subnet_ids)}")
            return vpc_id, subnet_ids
        except Exception as e:
            self.logger.error(f"Error setting up network: {str(e)}")
            raise

    def _setup_security_group(self, vpc_id: str) -> str:
        """Set up security group."""
        try:
            sg_name = f"midserver-{self.environment}-sg"
            sg_id = self.ec2_utils.create_security_group(sg_name, f"Security group for MID server {self.environment}", vpc_id)
            self.ec2_utils.authorize_security_group_ingress(sg_id, [
                {'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443, 'CidrIp': '0.0.0.0/0'},
                {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'CidrIp': '0.0.0.0/0'}
            ])
            self.logger.info(f"Created security group: {sg_id}")
            return sg_id
        except Exception as e:
            self.logger.error(f"Error setting up security group: {str(e)}")
            raise

    def _setup_iam_roles(self) -> tuple:
        """Set up IAM roles for ECS tasks."""
        try:
            task_role_name = f"midserver-{self.environment}-task-role"
            execution_role_name = f"midserver-{self.environment}-execution-role"

            task_role = self._create_or_get_role(task_role_name, "ecs-tasks.amazonaws.com")
            execution_role = self._create_or_get_role(execution_role_name, "ecs-tasks.amazonaws.com")

            self.iam_utils.attach_role_policy(task_role_name, "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess")
            self.iam_utils.attach_role_policy(execution_role_name, "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy")

            self.logger.info(f"Set up IAM roles: {task_role_name}, {execution_role_name}")
            return task_role['Role']['Arn'], execution_role['Role']['Arn']
        except Exception as e:
            self.logger.error(f"Error setting up IAM roles: {str(e)}")
            raise

    def _create_or_get_role(self, role_name: str, service: str) -> Dict[str, Any]:
        """Create a new role or get an existing one."""
        role = self.iam_utils.get_role(role_name)
        if not role:
            trust_relationship = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": service
                        },
                        "Action": "sts:AssumeRole"
                    }
                ]
            }
            role = self.iam_utils.create_role(role_name, json.dumps(trust_relationship))
        return role

    def _setup_ecs_cluster(self) -> str:
        """Set up ECS cluster."""
        try:
            cluster_name = f"midserver-{self.environment}-cluster"
            self.ecs_utils.create_cluster(cluster_name)
            self.logger.info(f"Created ECS cluster: {cluster_name}")
            return cluster_name
        except Exception as e:
            self.logger.error(f"Error setting up ECS cluster: {str(e)}")
            raise

    def _register_task_definition(self, task_role_arn: str, execution_role_arn: str) -> str:
        """Register ECS task definition."""
        try:
            family = f"midserver-{self.environment}-task"
            container_definitions = [
                {
                    "name": f"midserver-{self.environment}",
                    "image": f"{os.environ.get('ECR_REPO')}:latest",  # Ensure ECR_REPO is set in environment variables
                    "cpu": 256,
                    "memory": 512,
                    "essential": True,
                    "portMappings": [],
                    "environment": self._get_environment_variables(),
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-group": f"/ecs/midserver-{self.environment}",
                            "awslogs-region": os.environ.get("AWS_REGION", "us-east-1"),
                            "awslogs-stream-prefix": "ecs"
                        }
                    }
                }
            ]

            response = self.ecs_utils.register_task_definition(
                family=family,
                container_definitions=container_definitions,
                task_role_arn=task_role_arn,
                execution_role_arn=execution_role_arn
            )

            task_definition_arn = response['taskDefinition']['taskDefinitionArn']
            self.logger.info(f"Registered task definition: {task_definition_arn}")
            return task_definition_arn
        except Exception as e:
            self.logger.error(f"Error registering task definition: {str(e)}")
            raise

    def _get_environment_variables(self) -> List[Dict[str, str]]:
        """Get environment variables for the MID server container."""
        try:
            env_vars = [
                {"name": "MID_INSTANCE_URL", "value": self.ssm_utils.get_parameter(f"/midserver/{self.environment}/MID_INSTANCE_URL")},
                {"name": "MID_INSTANCE_USERNAME", "value": self.ssm_utils.get_parameter(f"/midserver/{self.environment}/MID_INSTANCE_USERNAME")},
                {"name": "MID_INSTANCE_PASSWORD", "value": self.ssm_utils.get_parameter(f"/midserver/{self.environment}/MID_INSTANCE_PASSWORD")},
                {"name": "MID_SERVER_NAME", "value": self.ssm_utils.get_parameter(f"/midserver/{self.environment}/MID_SERVER_NAME")}
            ]
            return env_vars
        except Exception as e:
            self.logger.error(f"Error getting environment variables: {str(e)}")
            raise

    def _setup_ecs_service(self, cluster_name: str, task_definition_arn: str, subnet_ids: List[str], security_groups: List[str]):
        """Create or update ECS service."""
        try:
            service_name = f"midserver-{self.environment}-service"
            
            # Check if the service already exists
            existing_services = self.ecs_utils.describe_services(cluster_name, [service_name])
            
            if existing_services['services']:
                # Update existing service
                self.ecs_utils.update_service(
                    cluster=cluster_name,
                    service=service_name,
                    taskDefinition=task_definition_arn,
                    desiredCount=1,
                    networkConfiguration={
                        'awsvpcConfiguration': {
                            'subnets': subnet_ids,
                            'securityGroups': security_groups,
                            'assignPublicIp': 'ENABLED'
                        }
                    }
                )
                self.logger.info(f"Updated existing ECS service: {service_name}")
            else:
                # Create new service
                self.ecs_utils.create_service(
                    cluster=cluster_name,
                    serviceName=service_name,
                    taskDefinition=task_definition_arn,
                    desiredCount=1,
                    launchType='FARGATE',
                    networkConfiguration={
                        'awsvpcConfiguration': {
                            'subnets': subnet_ids,
                            'securityGroups': security_groups,
                            'assignPublicIp': 'ENABLED'
                        }
                    }
                )
                self.logger.info(f"Created new ECS service: {service_name}")
        except Exception as e:
            self.logger.error(f"Error setting up ECS service: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    deployer = MIDServerDeployer(profile_name="default", environment="dev")
    deployer.deploy()