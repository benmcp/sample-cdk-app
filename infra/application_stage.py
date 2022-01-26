import os
from aws_cdk import (
    Duration,
    Stage,
    aws_lambda as _lambda,
    aws_apigateway as apigateway
)
from constructs import Construct
from dotenv import load_dotenv

from .application_stack import ApplicationStack

load_dotenv()

class ApplicationStage(Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        application_name: str = os.getenv('APPLICATION')

        _application_stack = ApplicationStack(
            self,
            f'{application_name}-ApplicationStack'
        )
