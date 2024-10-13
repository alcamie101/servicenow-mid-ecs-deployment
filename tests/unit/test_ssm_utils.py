import unittest
from unittest.mock import patch, MagicMock
from src.aws_utils.ssm import SSMUtils


class TestSSMUtils(unittest.TestCase):

    def setUp(self):
        self.ssm_utils = SSMUtils(profile_name="test_profile")

    @patch("src.aws_utils.ssm.AWSUtils.aws_cmd")
    def test_put_parameter(self, mock_aws_cmd):
        # Arrange
        name = "/test/parameter"
        value = "test-value"
        description = "Test parameter"
        param_type = "SecureString"
        mock_response = {"Version": 1}
        mock_aws_cmd.return_value = mock_response

        # Act
        result = self.ssm_utils.put_parameter(name, value, description, param_type)

        # Assert
        mock_aws_cmd.assert_called_once_with(
            "ssm",
            "put_parameter",
            Name=name,
            Value=value,
            Description=description,
            Type=param_type,
            Overwrite=False,
        )
        self.assertEqual(result, mock_response)

    @patch("src.aws_utils.ssm.AWSUtils.aws_cmd")
    def test_get_parameter(self, mock_aws_cmd):
        # Arrange
        name = "/test/parameter"
        mock_response = {"Parameter": {"Value": "test-value"}}
        mock_aws_cmd.return_value = mock_response

        # Act
        result = self.ssm_utils.get_parameter(name)

        # Assert
        mock_aws_cmd.assert_called_once_with(
            "ssm", "get_parameter", Name=name, WithDecryption=True
        )
        self.assertEqual(result, "test-value")

    @patch("src.aws_utils.ssm.AWSUtils.aws_cmd")
    def test_delete_parameter(self, mock_aws_cmd):
        # Arrange
        name = "/test/parameter"

        # Act
        self.ssm_utils.delete_parameter(name)

        # Assert
        mock_aws_cmd.assert_called_once_with("ssm", "delete_parameter", Name=name)

    @patch("src.aws_utils.ssm.AWSUtils.aws_cmd")
    def test_get_parameters_by_path(self, mock_aws_cmd):
        # Arrange
        path = "/test/"
        mock_response = {
            "Parameters": [
                {"Name": "/test/param1", "Value": "value1"},
                {"Name": "/test/param2", "Value": "value2"},
            ]
        }
        mock_aws_cmd.return_value = mock_response

        # Act
        result = self.ssm_utils.get_parameters_by_path(path)

        # Assert
        mock_aws_cmd.assert_called_once_with(
            "ssm",
            "get_parameters_by_path",
            Path=path,
            Recursive=True,
            WithDecryption=True,
        )
        self.assertEqual(result, mock_response["Parameters"])


if __name__ == "__main__":
    unittest.main()
