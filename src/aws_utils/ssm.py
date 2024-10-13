from . import AWSUtils
from typing import Dict, Any, List, Optional


class SSMUtils(AWSUtils):
    def __init__(self, profile_name=None):
        super().__init__(profile_name)
        self.ssm_client = self.session.client("ssm")

    def put_parameter(
        self,
        name: str,
        value: str,
        description: str,
        param_type: str = "SecureString",
        overwrite: bool = False,
    ) -> Dict[str, Any]:
        """
        Create or update a parameter in SSM Parameter Store.

        :param name: Name of the parameter
        :param value: Value of the parameter
        :param description: Description of the parameter
        :param param_type: Type of the parameter (String, StringList, or SecureString)
        :param overwrite: Whether to overwrite an existing parameter
        :return: Dictionary containing the response from SSM
        """
        return self.aws_cmd(
            "ssm",
            "put_parameter",
            Name=name,
            Value=value,
            Description=description,
            Type=param_type,
            Overwrite=overwrite,
        )

    def get_parameter(self, name: str, with_decryption: bool = True) -> Optional[str]:
        """
        Get a parameter from SSM Parameter Store.

        :param name: Name of the parameter
        :param with_decryption: Whether to decrypt the parameter value
        :return: Parameter value, or None if the parameter doesn't exist
        """
        try:
            response = self.aws_cmd(
                "ssm", "get_parameter", Name=name, WithDecryption=with_decryption
            )
            return response["Parameter"]["Value"]
        except self.ssm_client.exceptions.ParameterNotFound:
            return None

    def delete_parameter(self, name: str) -> None:
        """
        Delete a parameter from SSM Parameter Store.

        :param name: Name of the parameter to delete
        """
        try:
            self.aws_cmd("ssm", "delete_parameter", Name=name)
        except self.ssm_client.exceptions.ParameterNotFound:
            self.logger.warning(f"Parameter {name} not found, skipping deletion.")

    def get_parameters_by_path(
        self, path: str, recursive: bool = True, with_decryption: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get parameters by path from SSM Parameter Store.

        :param path: Path to get parameters from
        :param recursive: Whether to recursively get parameters
        :param with_decryption: Whether to decrypt the parameter values
        :return: List of dictionaries containing parameter information
        """
        response = self.aws_cmd(
            "ssm",
            "get_parameters_by_path",
            Path=path,
            Recursive=recursive,
            WithDecryption=with_decryption,
        )
        return response["Parameters"]


# Example usage
if __name__ == "__main__":
    ssm_utils = SSMUtils()
    profile = ssm_utils.select_profile()
    ssm_utils = SSMUtils(profile_name=profile)

    # Example: Put a parameter
    ssm_utils.put_parameter(
        name="/midserver/dev/example_param",
        value="example_value",
        description="An example parameter",
        param_type="SecureString",
        overwrite=True,
    )
    print("Parameter put successfully")

    # Example: Get a parameter
    param_value = ssm_utils.get_parameter("/midserver/dev/example_param")
    print(f"Retrieved parameter value: {param_value}")

    # Example: Get parameters by path
    params = ssm_utils.get_parameters_by_path("/midserver/dev/")
    print(f"Parameters under /midserver/dev/: {params}")

    # Example: Delete a parameter (uncomment to test)
    # ssm_utils.delete_parameter('/midserver/dev/example_param')
    # print("Parameter deleted successfully")
