from lambdas.health.handler import handler

def test_health():
    """Test Health Endpoint
    """
    try:
        reaponse = handler({}, {})

        assert reaponse['statusCode'] == 200

    except Exception: # pylint: disable=broad-except
        assert False
