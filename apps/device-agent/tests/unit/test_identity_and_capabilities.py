from pathlib import Path

from device_agent.capabilities.detector import CapabilityDetector
from device_agent.core.identity import load_or_create_agent_id


def test_persistent_identity_survives_restart(tmp_path: Path) -> None:
    first = load_or_create_agent_id(tmp_path)
    second = load_or_create_agent_id(tmp_path)

    assert first == second


def test_capability_detector_reports_expected_names() -> None:
    reports = CapabilityDetector().detect()

    assert {report.name for report in reports} == {"android.adb", "android.u2"}
