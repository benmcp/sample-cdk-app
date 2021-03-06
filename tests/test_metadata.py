"""Metadata API Pytest"""
from lambdas.metadata.handler import handler

def test_metadata():
    """Test Metadata Endpoint
    """
    try:
        reaponse = handler({}, {})

        assert reaponse['statusCode'] == 200

    except Exception: # pylint: disable=broad-except
        assert False
