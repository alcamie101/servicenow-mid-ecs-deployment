provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "mid_server_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "mid-server-vpc-${var.environment}"
  }
}

resource "aws_subnet" "mid_server_subnet" {
  count                   = 2
  vpc_id                  = aws_vpc.mid_server_vpc.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "mid-server-subnet-${var.environment}-${count.index + 1}"
  }
}

resource "aws_security_group" "mid_server_sg" {
  name        = "mid-server-sg-${var.environment}"
  description = "Security group for MID server"
  vpc_id      = aws_vpc.mid_server_vpc.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "mid-server-sg-${var.environment}"
  }
}

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

resource "aws_iam_role" "ecs_execution_role" {
  name = "ecs-execution-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution_role_policy" {
  role       = aws_iam_role.ecs_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role" "ecs_task_role" {
  name = "ecs-task-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_ssm_parameter" "mid_instance_password" {
  name  = "/midserver/${var.environment}/MID_INSTANCE_PASSWORD"
  type  = "SecureString"
  value = var.mid_instance_password
}

data "aws_availability_zones" "available" {}