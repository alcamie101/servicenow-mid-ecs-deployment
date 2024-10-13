import boto3
from botocore.exceptions import ClientError
import logging
from typing import Any, Dict, Optional


class AWSUtils:
    def __init__(self, profile_name: Optional[str] = None):
        self.session = boto3.Session(profile_name=profile_name)
        self.logger = logging.getLogger(__name__)

    def aws_cmd(self, service: str, operation: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Execute an AWS CLI command using boto3.

        :param service: AWS service (e.g., 'ec2', 's3', 'ecs')
        :param operation: Operation to perform (e.g., 'describe_instances')
        :param kwargs: Additional arguments for the operation
        :return: Response from AWS
        """
        try:
            client = self.session.client(service)
            response = getattr(client, operation)(**kwargs)
            return response
        except ClientError as e:
            self.logger.error(f"AWS operation failed: {e}")
            if "ExpiredToken" in str(e):
                self.logger.error(
                    "AWS SSO token has expired. Please run 'aws sso login' and try again."
                )
            raise

    def select_profile(self) -> str:
        """
        Allow user to select an AWS profile.

        :return: Selected profile name
        """
        available_profiles = self.session.available_profiles
        print("Available AWS profiles:")
        for i, profile in enumerate(available_profiles, 1):
            print(f"{i}) {profile}")

        while True:
            try:
                choice = int(input("Select a profile number: "))
                if 1 <= choice <= len(available_profiles):
                    selected_profile = available_profiles[choice - 1]
                    print(f"Selected profile: {selected_profile}")
                    return selected_profile
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def check_sso_login(self) -> None:
        """
        Check SSO login status and prompt for login if necessary.
        """
        try:
            self.aws_cmd("sts", "get_caller_identity")
            print("SSO session is valid.")
        except ClientError as e:
            if "ExpiredToken" in str(e):
                print(
                    "SSO session expired or not logged in. Please run 'aws sso login' and try again."
                )
                raise
            else:
                raise


# Example usage
if __name__ == "__main__":
    aws_utils = AWSUtils()
    profile = aws_utils.select_profile()
    aws_utils = AWSUtils(profile_name=profile)
    aws_utils.check_sso_login()
