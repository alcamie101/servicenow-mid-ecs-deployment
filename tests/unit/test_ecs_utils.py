import unittest
from unittest.mock import patch, MagicMock
from src.aws_utils.ecs import ECSUtils


class TestECSUtils(unittest.TestCase):

    def setUp(self):
        self.ecs_utils = ECSUtils(profile_name="test_profile")

    @patch("src.aws_utils.ecs.AWSUtils.aws_cmd")
    def test_list_clusters(self, mock_aws_cmd):
        # Arrange
        mock_response = {
            "clusterArns": ["arn:aws:ecs:us-east-1:123456789012:cluster/test-cluster"]
        }
        mock_aws_cmd.return_value = mock_response

        # Act
        result = self.ecs_utils.list_clusters()

        # Assert
        mock_aws_cmd.assert_called_once_with("ecs", "list_clusters")
        self.assertEqual(result, mock_response["clusterArns"])

    @patch("src.aws_utils.ecs.AWSUtils.aws_cmd")
    def test_create_cluster(self, mock_aws_cmd):
        # Arrange
        cluster_name = "test-cluster"
        mock_response = {"cluster": {"clusterName": cluster_name, "status": "ACTIVE"}}
        mock_aws_cmd.return_value = mock_response

        # Act
        result = self.ecs_utils.create_cluster(cluster_name)

        # Assert
        mock_aws_cmd.assert_called_once_with(
            "ecs", "create_cluster", clusterName=cluster_name
        )
        self.assertEqual(result, mock_response)

    @patch("src.aws_utils.ecs.AWSUtils.aws_cmd")
    def test_register_task_definition(self, mock_aws_cmd):
        # Arrange
        family = "test-task"
        container_definitions = [{"name": "test-container", "image": "test-image"}]
        task_role_arn = "arn:aws:iam::123456789012:role/test-task-role"
        execution_role_arn = "arn:aws:iam::123456789012:role/test-execution-role"
        mock_response = {
            "taskDefinition": {
                "taskDefinitionArn": "arn:aws:ecs:us-east-1:123456789012:task-definition/test-task:1"
            }
        }
        mock_aws_cmd.return_value = mock_response

        # Act
        result = self.ecs_utils.register_task_definition(
            family, container_definitions, task_role_arn, execution_role_arn
        )

        # Assert
        mock_aws_cmd.assert_called_once_with(
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
        self.assertEqual(result, mock_response)

    @patch("src.aws_utils.ecs.AWSUtils.aws_cmd")
    def test_create_service(self, mock_aws_cmd):
        # Arrange
        cluster = "test-cluster"
        service_name = "test-service"
        task_definition = (
            "arn:aws:ecs:us-east-1:123456789012:task-definition/test-task:1"
        )
        desired_count = 1
        subnets = ["subnet-12345678"]
        security_groups = ["sg-12345678"]
        mock_response = {"service": {"serviceName": service_name, "status": "ACTIVE"}}
        mock_aws_cmd.return_value = mock_response

        # Act
        result = self.ecs_utils.create_service(
            cluster,
            service_name,
            task_definition,
            desired_count,
            subnets,
            security_groups,
        )

        # Assert
        mock_aws_cmd.assert_called_once_with(
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
        self.assertEqual(result, mock_response)


if __name__ == "__main__":
    unittest.main()
