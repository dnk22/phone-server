from contracts import HealthResponse, HealthState


def test_health_response_serializes_to_wire_value() -> None:
    response = HealthResponse(status=HealthState.OK)

    assert response.model_dump(mode="json") == {"status": "ok", "service": "control-api"}
