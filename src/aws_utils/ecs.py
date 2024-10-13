from . import AWSUtils
from typing import List, Dict, Any, Optional


class ECSUtils(AWSUtils):
    def __init__(self, profile_name=None):
        super().__init__(profile_name)
        self.ecs_client = self.session.client("ecs")

    def list_clusters(self) -> List[str]:
        """
        List all ECS clusters.

        :return: List of cluster ARNs
        """
        response = self.aws_cmd("ecs", "list_clusters")
        return response["clusterArns"]

    def create_cluster(self, cluster_name: str) -> Dict[str, Any]:
        """
        Create a new ECS cluster.

        :param cluster_name: Name of the cluster to create
        :return: Dictionary containing cluster information
        """
        return self.aws_cmd("ecs", "create_cluster", clusterName=cluster_name)

    def register_task_definition(
        self,
        family: str,
        container_definitions: List[Dict[str, Any]],
        task_role_arn: str,
        execution_role_arn: str,
    ) -> Dict[str, Any]:
        """
        Register a new task definition.

        :param family: Family name of the task definition
        :param container_definitions: List of container definitions
        :param task_role_arn: ARN of the IAM role for the task
        :param execution_role_arn: ARN of the IAM role for task execution
        :return: Dictionary containing the registered task definition
        """
        return self.aws_cmd(
            "ecs",
            "register_task_definition",
            family=family,
            containerDefinitions=container_definitions,
            taskRoleArn=task_role_arn,
            executionRoleArn=execution_role_arn,
            networkMode="awsvpc",
            requiresCompatibilities=["FARGATE"],
            cpu="256",
            memory="512",
        )

    def create_service(
        self,
        cluster: str,
        service_name: str,
        task_definition: str,
        desired_count: int,
        subnets: List[str],
        security_groups: List[str],
    ) -> Dict[str, Any]:
        """
        Create a new ECS service.

        :param cluster: Name of the ECS cluster
        :param service_name: Name of the service to create
        :param task_definition: ARN of the task definition
        :param desired_count: Desired number of tasks
        :param subnets: List of subnet IDs
        :param security_groups: List of security group IDs
        :return: Dictionary containing service information
        """
        return self.aws_cmd(
            "ecs",
            "create_service",
            cluster=cluster,
            serviceName=service_name,
            taskDefinition=task_definition,
            desiredCount=desired_count,
            launchType="FARGATE",
            networkConfiguration={
                "awsvpcConfiguration": {
                    "subnets": subnets,
                    "securityGroups": security_groups,
                    "assignPublicIp": "ENABLED",
                }
            },
        )

    def describe_services(self, cluster: str, services: List[str]) -> Dict[str, Any]:
        """
        Describe ECS services.

        :param cluster: Name of the ECS cluster
        :param services: List of service names or ARNs
        :return: Dictionary containing service descriptions
        """
        return self.aws_cmd(
            "ecs", "describe_services", cluster=cluster, services=services
        )


# Example usage
if __name__ == "__main__":
    ecs_utils = ECSUtils()
    profile = ecs_utils.select_profile()
    ecs_utils = ECSUtils(profile_name=profile)

    # Example: List clusters
    clusters = ecs_utils.list_clusters()
    print(f"ECS Clusters: {clusters}")

    # Example: Create a cluster (uncomment to run)
    # new_cluster = ecs_utils.create_cluster('MyNewCluster')
    # print(f"Created cluster: {new_cluster}")
