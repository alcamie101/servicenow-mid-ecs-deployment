from . import AWSUtils
from typing import Dict, Any, List, Optional


class IAMUtils(AWSUtils):
    def __init__(self, profile_name=None):
        super().__init__(profile_name)
        self.iam_client = self.session.client("iam")

    def create_role(
        self, role_name: str, assume_role_policy_document: str
    ) -> Dict[str, Any]:
        """
        Create an IAM role.

        :param role_name: Name of the role to create
        :param assume_role_policy_document: JSON string of the trust relationship policy document
        :return: Dictionary containing the created role information
        """
        return self.aws_cmd(
            "iam",
            "create_role",
            RoleName=role_name,
            AssumeRolePolicyDocument=assume_role_policy_document,
        )

    def attach_role_policy(self, role_name: str, policy_arn: str) -> None:
        """
        Attach a policy to an IAM role.

        :param role_name: Name of the role
        :param policy_arn: ARN of the policy to attach
        """
        self.aws_cmd(
            "iam", "attach_role_policy", RoleName=role_name, PolicyArn=policy_arn
        )

    def create_policy(self, policy_name: str, policy_document: str) -> Dict[str, Any]:
        """
        Create an IAM policy.

        :param policy_name: Name of the policy to create
        :param policy_document: JSON string of the policy document
        :return: Dictionary containing the created policy information
        """
        return self.aws_cmd(
            "iam",
            "create_policy",
            PolicyName=policy_name,
            PolicyDocument=policy_document,
        )

    def get_role(self, role_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about an IAM role.

        :param role_name: Name of the role
        :return: Dictionary containing role information, or None if the role doesn't exist
        """
        try:
            return self.aws_cmd("iam", "get_role", RoleName=role_name)
        except self.iam_client.exceptions.NoSuchEntityException:
            return None

    def list_attached_role_policies(self, role_name: str) -> List[Dict[str, str]]:
        """
        List policies attached to an IAM role.

        :param role_name: Name of the role
        :return: List of dictionaries containing policy information
        """
        response = self.aws_cmd(
            "iam", "list_attached_role_policies", RoleName=role_name
        )
        return response["AttachedPolicies"]


# Example usage
if __name__ == "__main__":
    iam_utils = IAMUtils()
    profile = iam_utils.select_profile()
    iam_utils = IAMUtils(profile_name=profile)

    # Example: Get role information
    role_name = "example-role"
    role_info = iam_utils.get_role(role_name)
    if role_info:
        print(f"Role {role_name} exists: {role_info}")
    else:
        print(f"Role {role_name} does not exist")

    # Example: List attached policies for a role
    if role_info:
        policies = iam_utils.list_attached_role_policies(role_name)
        print(f"Policies attached to {role_name}: {policies}")

    # Note: Creating roles and policies is commented out to prevent accidental creation
    # Uncomment and modify as needed for testing

    # Example: Create a role (uncomment to test)
    # assume_role_policy = {
    #     "Version": "2012-10-17",
    #     "Statement": [
    #         {
    #             "Effect": "Allow",
    #             "Principal": {
    #                 "Service": "ecs-tasks.amazonaws.com"
    #             },
    #             "Action": "sts:AssumeRole"
    #         }
    #     ]
    # }
    # new_role = iam_utils.create_role("MyNewRole", json.dumps(assume_role_policy))
    # print(f"Created role: {new_role}")

    # Example: Attach a policy to a role (uncomment to test)
    # iam_utils.attach_role_policy("MyNewRole", "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy")
    # print("Attached AmazonECSTaskExecutionRolePolicy to MyNewRole")
