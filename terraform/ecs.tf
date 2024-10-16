resource "aws_ecs_cluster" "mid_server_cluster" {
  name = "mid-server-cluster-${var.environment}"

  tags = {
    Name = "mid-server-cluster-${var.environment}"
  }
}

resource "aws_ecs_task_definition" "mid_server_task" {
  family                   = "mid-server-task-${var.environment}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([{
    name  = "mid-server-container-${var.environment}"
    image = "${var.ecr_repo_url}:latest"
    portMappings = [{
      containerPort = 443
      hostPort      = 443
    }]
    environment = [
      { name = "MID_INSTANCE_URL", value = var.mid_instance_url },
      { name = "MID_INSTANCE_USERNAME", value = var.mid_instance_username },
      { name = "MID_SERVER_NAME", value = var.mid_server_name }
    ]
    secrets = [
      { name = "MID_INSTANCE_PASSWORD", valueFrom = aws_ssm_parameter.mid_instance_password.arn }
    ]
  }])
}

resource "aws_ecs_service" "mid_server_service" {
  name            = "mid-server-service-${var.environment}"
  cluster         = aws_ecs_cluster.mid_server_cluster.id
  task_definition = aws_ecs_task_definition.mid_server_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.mid_server_subnet[*].id
    security_groups  = [aws_security_group.mid_server_sg.id]
    assign_public_ip = true
  }
}