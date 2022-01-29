#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infra.codepipeline_stack import CodePipelineStack
from dotenv import load_dotenv

load_dotenv()

app = cdk.App()

application_name: str = os.getenv('APPLICATION')

CodePipelineStack(
    app,
    f'{application_name}-CodePipelineStack'
)

app.synth()


