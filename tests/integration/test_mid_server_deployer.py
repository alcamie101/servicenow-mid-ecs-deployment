import unittest
from unittest.mock import patch, MagicMock
from src.deployment.mid_server import MIDServerDeployer


class TestMIDServerDeployer(unittest.TestCase):

    def setUp(self):
        self.deployer = MIDServerDeployer(
            profile_name="test_profile", environment="test"
        )

    @patch("src.aws_utils.ec2.EC2Utils")
    @patch("src.aws_utils.ecs.ECSUtils")
    @patch("src.aws_utils.iam.IAMUtils")
    @patch("src.aws_utils.ssm.SSMUtils")
    def test_deploy(self, mock_ssm, mock_iam, mock_ecs, mock_ec2):
        # Arrange
        mock_ec2.return_value.describe_vpcs.return_value = {
            "Vpcs": [{"VpcId": "vpc-12345678"}]
        }
        mock_ec2.return_value.describe_subnets.return_value = {
            "Subnets": [{"SubnetId": "subnet-12345678"}]
        }
        mock_ec2.return_value.create_security_group.return_value = "sg-12345678"

        mock_iam.return_value.get_role.return_value = None
        mock_iam.return_value.create_role.return_value = {
            "Role": {"Arn": "arn:aws:iam::123456789012:role/test-role"}
        }

        mock_ecs.return_value.create_cluster.return_value = {
            "cluster": {"clusterName": "test-cluster"}
        }
        mock_ecs.return_value.register_task_definition.return_value = {
            "taskDefinition": {
                "taskDefinitionArn": "arn:aws:ecs:us-west-2:123456789012:task-definition/test:1"
            }
        }
        mock_ecs.return_value.describe_services.return_value = {"services": []}
        mock_ecs.return_value.create_service.return_value = {
            "service": {"serviceName": "test-service"}
        }

        mock_ssm.return_value.get_parameter.return_value = "test-value"

        # Act
        self.deployer.deploy()

        # Assert
        mock_ec2.return_value.describe_vpcs.assert_called_once()
        mock_ec2.return_value.describe_subnets.assert_called_once()
        mock_ec2.return_value.create_security_group.assert_called_once()

        mock_iam.return_value.get_role.assert_called()
        mock_iam.return_value.create_role.assert_called()
        mock_iam.return_value.attach_role_policy.assert_called()

        mock_ecs.return_value.create_cluster.assert_called_once()
        mock_ecs.return_value.register_task_definition.assert_called_once()
        mock_ecs.return_value.describe_services.assert_called_once()
        mock_ecs.return_value.create_service.assert_called_once()

        mock_ssm.return_value.get_parameter.assert_called()


if __name__ == "__main__":
    unittest.main()
