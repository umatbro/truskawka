import aws_cdk as cdk
from stack.infra_stack import InfraStack

app = cdk.App()
InfraStack(app, "qa")
InfraStack(app, "prod")

app.synth()
