"""Metadata Module"""
import os
import json
from dotenv import load_dotenv
from aws_lambda_powertools.utilities.typing import LambdaContext

load_dotenv()

def handler(_event: dict, _context: LambdaContext) -> dict:
    """Meetadata API Lambda

    :param _event: API Gateway Event
    :type _event: dict
    :param _context: AWS Lambda Cotext
    :type _context: LambdaContext
    :return: HTTP Response
    :rtype: dict
    """

    print(os.environ)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'myApplication': [
                {
                    'version': '1.0', # TODO
                    'description' : 'technical test', # TODO
                    'lastcommit': 'c0484c' # TODO
                }
            ]
        })
    }
