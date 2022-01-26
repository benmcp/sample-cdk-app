import os
from typing import List
from aws_cdk import (
    aws_lambda as _lambda,
    aws_ssm as _ssm,
    Stack
)
from constructs import Construct
from dotenv import load_dotenv

load_dotenv()


class LambdaLayerStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        application_name: str = os.getenv('APPLICATION')

        layer_name: str = f"{application_name}-venv-layer"
        layer_param_name: str = f"/{application_name}/venvLayer"

        requirements_file = open('requirements-lambda.txt', "r")

        data = requirements_file.read()

        commands: List[str] = [
            f"echo '{data}' > requirements.txt",
            'pip install -r requirements.txt -t /asset-output/python',
            'cp -au . /asset-output'
        ]

        command_str: str = ' && '.join(commands)

        self.layer = _lambda.LayerVersion(
            self,
            layer_name,
            code=_lambda.Code.from_asset('.layer',
                bundling={
                    "image": getattr(_lambda.Runtime.PYTHON_3_9, 'bundling_image'),
                    "command": [
                        "bash",
                        "-c",
                        command_str
                    ]
                }
            ),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
            license="Apache-2.0",
            description="Python Packages from requirements"
        )

        self.ssm = _ssm.StringParameter(
            self,
            'LambdaVersionArn',
            parameter_name=layer_param_name,
            string_value=self.layer.layer_version_arn
        )
