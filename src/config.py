import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ENV = os.getenv('ENVIRONMENT', 'dev')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    
    # Environment-specific configurations
    CONFIGS = {
        'dev': {
            'ECR_REPO': 'your-dev-ecr-repo-url',
            'MID_INSTANCE_URL': 'https://dev.service-now.com',
            'MID_SERVER_NAME': 'mid-server-dev',
        },
        'staging': {
            'ECR_REPO': 'your-staging-ecr-repo-url',
            'MID_INSTANCE_URL': 'https://staging.service-now.com',
            'MID_SERVER_NAME': 'mid-server-staging',
        },
        'prod': {
            'ECR_REPO': 'your-prod-ecr-repo-url',
            'MID_INSTANCE_URL': 'https://prod.service-now.com',
            'MID_SERVER_NAME': 'mid-server-prod',
        }
    }
    
    @classmethod
    def get(cls, key):
        return cls.CONFIGS[cls.ENV].get(key)

# Usage:
# from config import Config
# ecr_repo = Config.get('ECR_REPO')