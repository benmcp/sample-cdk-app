import os
from aws_cdk.pipelines import (
    CodePipeline,
    CodeBuildOptions,
    CodePipelineSource,
    ShellStep
)
from aws_cdk import (
    Stack,
    SecretValue,
    aws_codebuild,
    aws_codepipeline_actions as codepipeline_actions
)
from constructs import Construct
from dotenv import load_dotenv

from .application_stage import ApplicationStage
from .lambda_layer_stage import LambdaLayerStage


load_dotenv()

class CodePipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        application_name: str = os.getenv('APPLICATION')

        # Declare Pipeline Source
        code_source = CodePipelineSource.git_hub(
            repo_string="benmcp/sample-cdk-app",
            branch='main',
            authentication=SecretValue.secrets_manager('github-token')
        )

        git_source_version_raw = os.getenv('CODEBUILD_RESOLVED_SOURCE_VERSION')

        git_source_version = 'None'

        if git_source_version_raw:
            git_source_version = git_source_version_raw

        # Declare Pipeline Buile Process
        pipeline = CodePipeline(
            self,
            f'{application_name}-pipeline',
            pipeline_name=f'{application_name}-pipeline',
            code_build_defaults=CodeBuildOptions(
                build_environment=aws_codebuild.BuildEnvironment(
                    build_image=aws_codebuild.LinuxBuildImage.AMAZON_LINUX_2_3,
                    environment_variables={
                        'APPLICATION': aws_codebuild.BuildEnvironmentVariable(
                            value=application_name
                        )
                    }
                )
            ),
            docker_enabled_for_synth=True,
            synth=ShellStep(
                f'{application_name}-synth',
                input=code_source,
                commands=[
                    f'echo "GIT_COMMIT={git_source_version}" >> .env',
                    'npm install -g aws-cdk',
                    'python3 -m venv .venv',
                    'source .venv/bin/activate',
                    'pip3 install -r requirements.txt',
                    f'cdk synth {application_name}-CodePipelineStack',
                    'ls -la'
                ],
                primary_output_directory='cdk.out'
            )
        )

        layer_stack = LambdaLayerStage(
            self,
            'LambdaStage'
        )

        pipeline.add_stage(
            layer_stack
        )

        # Declare Pipeline Deployment
        app_stack = ApplicationStage(
            self,
            'AppStage'
        )

        pipeline.add_stage(app_stack)
