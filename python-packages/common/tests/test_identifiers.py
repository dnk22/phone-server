import pytest
from common import normalize_identifier


def test_normalize_identifier() -> None:
    assert normalize_identifier(" Device-01 ") == "device-01"


def test_normalize_identifier_rejects_empty_value() -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        normalize_identifier("   ")
