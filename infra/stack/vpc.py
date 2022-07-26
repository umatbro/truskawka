import aws_cdk.aws_ec2 as ec2
from aws_cdk import Stack
from constructs import Construct


class VPCStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(self, "Truskawa-VPC", cidr="10.0.0.0/16")
