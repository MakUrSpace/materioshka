import os
import typing
from aws_cdk import (
    aws_lambda,
    aws_ecr,
    App, Aws, Duration, Stack
)
from constructs import Construct


class MaterioshkaStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        image_name    = "MaterioshkaSAM"
        ecr_image = aws_lambda.EcrImageCode.from_asset_image(
            directory = os.path.join(os.getcwd(), "SAMApp"))

        ## Lambda Function
        aws_lambda.Function(self,
          id            = "materioshkaSAMLambda",
          description   = "Lambda for Materioshka App",
          code          = ecr_image,
          ## Handler and Runtime must be *FROM_IMAGE* when provisioning Lambda from Container.
          handler       = aws_lambda.Handler.FROM_IMAGE,
          runtime       = aws_lambda.Runtime.FROM_IMAGE,
          environment   = {"baha":"world"},
          function_name = "materioshakSAM",
          memory_size   = 5144,
          reserved_concurrent_executions = 10,
          timeout       = Duration.seconds(500),
        )


app = App()
env = {'region': 'us-east-1'}
MaterioshkaStack(app, "MaterioshkaStack", env=env)
app.synth()

