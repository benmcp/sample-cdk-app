import os
from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_ssm as _ssm,
    aws_apigateway as apigateway
)
from constructs import Construct
from dotenv import load_dotenv

load_dotenv()

class ApplicationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        application_name: str = os.getenv('APPLICATION')
        git_commit: str = os.getenv('GIT_COMMIT')

        if not git_commit:
            git_commit = "None"

        # Build up lambda layer (for packages)
        layer_param_name: str = f"/{application_name}/venvLayer"

        layer_arn: str = _ssm.StringParameter.value_for_string_parameter(
            self,
            layer_param_name
        )

        lambda_layer = _lambda.LayerVersion.from_layer_version_arn(
            self,
            "BaseLayerFromArn",
            layer_arn
        )

        # Simple root endpoint
        base_handler = _lambda.Function(
            self,
            f'{application_name}-APILambda',
            function_name=f'{application_name}-api-base',
            handler='base.handler.handler',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset('lambdas'),
            timeout=Duration.seconds(30),
            layers=[
                lambda_layer
            ]
        )

        api = apigateway.LambdaRestApi(
            self,
            f'{application_name}-rest-api',
            description=f'{application_name} REST API',
            deploy_options=None,
            handler=base_handler,
            proxy=False
        )

        base_url = api.root.add_resource('v1')

        base_url.add_method(http_method='GET')

        # Health endpoint
        health_handler = _lambda.Function(
            self,
            f'{application_name}-HealthLambda',
            function_name=f"{application_name}-api-health",
            handler='health.handler.handler',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset('lambdas'),
            timeout=Duration.seconds(30),
            layers=[
                lambda_layer
            ]
        )

        health_endpoint = base_url.add_resource('health')

        health_lambda_integration = apigateway.LambdaIntegration(health_handler)

        health_endpoint.add_method(
            http_method='GET',
            integration=health_lambda_integration
        )

        # metadata endpoint
        metadata_handler = _lambda.Function(
            self,
            f'{application_name}-MetadataFunction',
            function_name=f"{application_name}-api-metadata",
            handler='metadata.handler.handler',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset('lambdas'),
            timeout=Duration.seconds(30),
            environment={
                'GIT_COMMIT': git_commit
            },
            layers=[
                lambda_layer
            ]
        )

        metadata_endpoint = base_url.add_resource('metadata')

        metadata_lambda_integration = apigateway.LambdaIntegration(metadata_handler)
        
        metadata_endpoint.add_method(
            http_method='GET',
            integration=metadata_lambda_integration
        )

