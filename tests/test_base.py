"""Base API Pytest"""
from lambdas.base.handler import handler

def test_base():
    """Test Base Endpoint
    """
    try:
        reaponse = handler({}, {})

        assert reaponse['statusCode'] == 200

    except Exception: # pylint: disable=broad-except
        assert False
