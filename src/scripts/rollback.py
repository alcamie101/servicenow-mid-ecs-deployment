import boto3
import argparse
from config import Config

def rollback_ecs_service(cluster_name, service_name, previous_task_definition):
    ecs_client = boto3.client('ecs', region_name=Config.AWS_REGION)
    
    try:
        response = ecs_client.update_service(
            cluster=cluster_name,
            service=service_name,
            taskDefinition=previous_task_definition
        )
        print(f"Rolled back service {service_name} to task definition {previous_task_definition}")
        return True
    except Exception as e:
        print(f"Rollback failed: {str(e)}")
        return False

def get_previous_task_definition(cluster_name, service_name):
    ecs_client = boto3.client('ecs', region_name=Config.AWS_REGION)
    
    response = ecs_client.describe_services(cluster=cluster_name, services=[service_name])
    current_task_definition = response['services'][0]['taskDefinition']
    
    task_definition_parts = current_task_definition.split(':')
    previous_revision = int(task_definition_parts[-1]) - 1
    
    if previous_revision < 1:
        return None
    
    return ':'.join(task_definition_parts[:-1] + [str(previous_revision)])

def main():
    parser = argparse.ArgumentParser(description='Rollback ECS service to previous task definition')
    parser.add_argument('--cluster', required=True, help='ECS cluster name')
    parser.add_argument('--service', required=True, help='ECS service name')
    
    args = parser.parse_args()
    
    previous_task_definition = get_previous_task_definition(args.cluster, args.service)
    
    if previous_task_definition:
        success = rollback_ecs_service(args.cluster, args.service, previous_task_definition)
        if success:
            print("Rollback completed successfully")
        else:
            print("Rollback failed")
    else:
        print("No previous task definition found. Rollback not possible.")

if __name__ == "__main__":
    main()

# Usage: python rollback.py --cluster your-cluster-name --service your-service-name