import aws_cdk.aws_elasticbeanstalk as bs
from aws_cdk import Stack
from constructs import Construct

from dependencies import get_settings

# from infra.stack.rds_stack import RdsStack

settings = get_settings()


class InfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # role: Optional[iam.Role] = None
        # if settings.is_ng_env:
        #     role = iam.Role.from_role_arn(
        #         self, "NgRole", "arn:aws:iam::690296641723:role/netguru-devs"
        #     )

        application = bs.CfnApplication(
            self,
            "StrawberryApplication",
            application_name="strawberry",
        )

        bs.CfnEnvironment(
            self,
            "StrawberryEnvironment",
            application_name=application.application_name,
            cname_prefix="strawberry",
            description="Strawberry app test",
            environment_name="StrawberryEnvironment",
            # operations_role=role.role_arn,
            solution_stack_name="64bit Amazon Linux 2 v3.4.13 running Docker",
        )
