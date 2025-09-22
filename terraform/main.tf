terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"
}

variable "dockerhub_username" {
  description = "soumyachauhan"
  type        = string
}

variable "key_pair_name" {
  description = "mlops"
  type        = string
}

resource "aws_instance" "mlops-capstone" {
  ami           = "ami-0dee22c13ea7a9a67" # Amazon Linux 2 AMI in ap-south-1
  instance_type = "t3.micro"
  key_name      = var.key_pair_name

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              amazon-linux-extras install docker -y
              service docker start
              usermod -a -G docker ec2-user
              docker run -d -p 80:8000 ${var.dockerhub_username}/mlops-capstone:latest
              EOF

  tags = {
    Name = "mlops-capstone"
  }
}

output "instance_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.mlops-capstone.public_ip
}