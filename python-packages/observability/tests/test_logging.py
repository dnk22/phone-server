from observability import get_logger


def test_get_logger_returns_named_logger() -> None:
    assert get_logger("android-linux-server").name == "android-linux-server"
