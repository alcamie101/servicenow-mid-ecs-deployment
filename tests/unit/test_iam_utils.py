import unittest
from unittest.mock import patch, MagicMock
from src.aws_utils.iam import IAMUtils


class TestIAMUtils(unittest.TestCase):

    def setUp(self):
        self.iam_utils = IAMUtils(profile_name="test_profile")

    @patch("src.aws_utils.iam.AWSUtils.aws_cmd")
    def test_create_role(self, mock_aws_cmd):
        # Arrange
        role_name = "test-role"
        assume_role_policy_document = '{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "ecs-tasks.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
        mock_response = {
            "Role": {
                "RoleName": role_name,
                "Arn": f"arn:aws:iam::123456789012:role/{role_name}",
            }
        }
        mock_aws_cmd.return_value = mock_response

        # Act
        result = self.iam_utils.create_role(role_name, assume_role_policy_document)

        # Assert
        mock_aws_cmd.assert_called_once_with(
            "iam",
            "create_role",
            RoleName=role_name,
            AssumeRolePolicyDocument=assume_role_policy_document,
        )
        self.assertEqual(result, mock_response)

    @patch("src.aws_utils.iam.AWSUtils.aws_cmd")
    def test_attach_role_policy(self, mock_aws_cmd):
        # Arrange
        role_name = "test-role"
        policy_arn = "arn:aws:iam::aws:policy/AmazonECS_FullAccess"

        # Act
        self.iam_utils.attach_role_policy(role_name, policy_arn)

        # Assert
        mock_aws_cmd.assert_called_once_with(
            "iam", "attach_role_policy", RoleName=role_name, PolicyArn=policy_arn
        )

    @patch("src.aws_utils.iam.AWSUtils.aws_cmd")
    def test_create_policy(self, mock_aws_cmd):
        # Arrange
        policy_name = "test-policy"
        policy_document = '{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": "s3:ListBucket", "Resource": "arn:aws:s3:::example_bucket"}]}'
        mock_response = {
            "Policy": {
                "PolicyName": policy_name,
                "Arn": f"arn:aws:iam::123456789012:policy/{policy_name}",
            }
        }
        mock_aws_cmd.return_value = mock_response

        # Act
        result = self.iam_utils.create_policy(policy_name, policy_document)

        # Assert
        mock_aws_cmd.assert_called_once_with(
            "iam",
            "create_policy",
            PolicyName=policy_name,
            PolicyDocument=policy_document,
        )
        self.assertEqual(result, mock_response)

    @patch("src.aws_utils.iam.AWSUtils.aws_cmd")
    def test_get_role(self, mock_aws_cmd):
        # Arrange
        role_name = "test-role"
        mock_response = {
            "Role": {
                "RoleName": role_name,
                "Arn": f"arn:aws:iam::123456789012:role/{role_name}",
            }
        }
        mock_aws_cmd.return_value = mock_response

        # Act
        result = self.iam_utils.get_role(role_name)

        # Assert
        mock_aws_cmd.assert_called_once_with("iam", "get_role", RoleName=role_name)
        self.assertEqual(result, mock_response)

    @patch("src.aws_utils.iam.AWSUtils.aws_cmd")
    def test_list_attached_role_policies(self, mock_aws_cmd):
        # Arrange
        role_name = "test-role"
        mock_response = {
            "AttachedPolicies": [
                {
                    "PolicyName": "AmazonECS_FullAccess",
                    "PolicyArn": "arn:aws:iam::aws:policy/AmazonECS_FullAccess",
                }
            ]
        }
        mock_aws_cmd.return_value = mock_response

        # Act
        result = self.iam_utils.list_attached_role_policies(role_name)

        # Assert
        mock_aws_cmd.assert_called_once_with(
            "iam", "list_attached_role_policies", RoleName=role_name
        )
        self.assertEqual(result, mock_response["AttachedPolicies"])


if __name__ == "__main__":
    unittest.main()
