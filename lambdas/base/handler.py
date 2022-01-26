"""Base API Module"""
import json

from aws_lambda_powertools.utilities.typing import LambdaContext

def handler(_event: dict, _context: LambdaContext) -> dict:
    """Base API Lambda

    :param _event: API Gateway Event
    :type _event: dict
    :param _context: AWS Lambda Cotext
    :type _context: LambdaContext
    :return: HTTP Response
    :rtype: dict
    """

    return {
        'statusCode': 200,
        'headers': { 
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'title': 'hello world'
        })
    }
