import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as rds
from aws_cdk import SecretValue
from constructs import Construct

# from aws_cdk.aws_ec2 import InstanceType
from infra.stack.vpc import VPCStack


class RdsStack(VPCStack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.birthday_db = rds.DatabaseInstance(
            self,
            "Database",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_11_15
            ),
            credentials=rds.Credentials.from_password(
                "postgresuser", SecretValue("secret_pw")
            ),
            instance_type=ec2.InstanceType("t3.micro"),
            database_name="birthdaydb",
            vpc=self.vpc,
        )
