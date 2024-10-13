import unittest
from unittest.mock import patch, MagicMock
from src.aws_utils.ec2 import EC2Utils


class TestEC2Utils(unittest.TestCase):

    def setUp(self):
        self.ec2_utils = EC2Utils(profile_name="test_profile")

    @patch("src.aws_utils.ec2.AWSUtils.aws_cmd")
    def test_describe_vpcs(self, mock_aws_cmd):
        # Arrange
        mock_response = {"Vpcs": [{"VpcId": "vpc-12345678"}]}
        mock_aws_cmd.return_value = mock_response

        # Act
        result = self.ec2_utils.describe_vpcs()

        # Assert
        mock_aws_cmd.assert_called_once_with("ec2", "describe_vpcs")
        self.assertEqual(result, mock_response)

    @patch("src.aws_utils.ec2.AWSUtils.aws_cmd")
    def test_describe_subnets(self, mock_aws_cmd):
        # Arrange
        vpc_id = "vpc-12345678"
        mock_response = {"Subnets": [{"SubnetId": "subnet-12345678"}]}
        mock_aws_cmd.return_value = mock_response

        # Act
        result = self.ec2_utils.describe_subnets(vpc_id)

        # Assert
        mock_aws_cmd.assert_called_once_with(
            "ec2", "describe_subnets", Filters=[{"Name": "vpc-id", "Values": [vpc_id]}]
        )
        self.assertEqual(result, mock_response)

    @patch("src.aws_utils.ec2.AWSUtils.aws_cmd")
    def test_create_security_group(self, mock_aws_cmd):
        # Arrange
        group_name = "test-sg"
        description = "Test security group"
        vpc_id = "vpc-12345678"
        mock_response = {"GroupId": "sg-87654321"}
        mock_aws_cmd.return_value = mock_response

        # Act
        result = self.ec2_utils.create_security_group(group_name, description, vpc_id)

        # Assert
        mock_aws_cmd.assert_called_once_with(
            "ec2",
            "create_security_group",
            GroupName=group_name,
            Description=description,
            VpcId=vpc_id,
        )
        self.assertEqual(result, "sg-87654321")

    @patch("src.aws_utils.ec2.AWSUtils.aws_cmd")
    def test_authorize_security_group_ingress(self, mock_aws_cmd):
        # Arrange
        group_id = "sg-87654321"
        ip_permissions = [
            {"IpProtocol": "tcp", "FromPort": 80, "ToPort": 80, "CidrIp": "0.0.0.0/0"}
        ]

        # Act
        self.ec2_utils.authorize_security_group_ingress(group_id, ip_permissions)

        # Assert
        mock_aws_cmd.assert_called_once_with(
            "ec2",
            "authorize_security_group_ingress",
            GroupId=group_id,
            IpPermissions=ip_permissions,
        )


if __name__ == "__main__":
    unittest.main()
