import os
import argparse
import logging
from dotenv import load_dotenv
from src.deployment.mid_server import MIDServerDeployer

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_environment_variables():
    load_dotenv()
    return {
        "AWS_PROFILE": os.getenv("AWS_PROFILE"),
        "AWS_REGION": os.getenv("AWS_REGION"),
        "ENVIRONMENT": os.getenv("ENVIRONMENT", "dev"),
    }


def validate_environment(env):
    valid_environments = ["dev", "staging", "prod"]
    if env not in valid_environments:
        raise ValueError(
            f"Invalid environment: {env}. Must be one of {valid_environments}"
        )


def deploy(environment):
    try:
        validate_environment(environment)
        env_vars = load_environment_variables()

        logger.info(f"Starting deployment for environment: {environment}")

        deployer = MIDServerDeployer(
            profile_name=env_vars["AWS_PROFILE"], environment=environment
        )
        deployer.deploy()

        logger.info(f"Deployment completed successfully for environment: {environment}")
    except Exception as e:
        logger.error(f"Deployment failed: {str(e)}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Deploy ServiceNow MID Server to AWS ECS"
    )
    parser.add_argument(
        "--env",
        type=str,
        default="dev",
        help="Deployment environment (dev/staging/prod)",
    )
    args = parser.parse_args()

    deploy(args.env)
