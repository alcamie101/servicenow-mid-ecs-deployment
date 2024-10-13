from . import AWSUtils
from typing import List, Dict, Any


class EC2Utils(AWSUtils):
    def __init__(self, profile_name=None):
        super().__init__(profile_name)
        self.ec2_client = self.session.client("ec2")

    def describe_vpcs(self, filters: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Describe VPCs with optional filters.

        :param filters: List of filters to apply
        :return: Dictionary containing VPC information
        """
        kwargs = {"Filters": filters} if filters else {}
        return self.aws_cmd("ec2", "describe_vpcs", **kwargs)

    def describe_subnets(self, vpc_id: str) -> Dict[str, Any]:
        """
        Describe subnets for a given VPC.

        :param vpc_id: ID of the VPC
        :return: Dictionary containing subnet information
        """
        filters = [{"Name": "vpc-id", "Values": [vpc_id]}]
        return self.aws_cmd("ec2", "describe_subnets", Filters=filters)

    def create_security_group(
        self, group_name: str, description: str, vpc_id: str
    ) -> str:
        """
        Create a new security group.

        :param group_name: Name of the security group
        :param description: Description of the security group
        :param vpc_id: ID of the VPC to create the security group in
        :return: ID of the created security group
        """
        response = self.aws_cmd(
            "ec2",
            "create_security_group",
            GroupName=group_name,
            Description=description,
            VpcId=vpc_id,
        )
        return response["GroupId"]

    def authorize_security_group_ingress(
        self, group_id: str, ip_permissions: List[Dict[str, Any]]
    ) -> None:
        """
        Authorize ingress rules for a security group.

        :param group_id: ID of the security group
        :param ip_permissions: List of IP permissions to authorize
        """
        self.aws_cmd(
            "ec2",
            "authorize_security_group_ingress",
            GroupId=group_id,
            IpPermissions=ip_permissions,
        )


# Example usage
if __name__ == "__main__":
    ec2_utils = EC2Utils()
    profile = ec2_utils.select_profile()
    ec2_utils = EC2Utils(profile_name=profile)

    # Example: Describe VPCs
    vpcs = ec2_utils.describe_vpcs()
    print(f"VPCs: {vpcs}")

    # Example: Create a security group (make sure to replace 'vpc-id' with an actual VPC ID)
    # sg_id = ec2_utils.create_security_group('MySecurityGroup', 'My security group description', 'vpc-id')
    # print(f"Created security group: {sg_id}")
