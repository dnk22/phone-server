import importlib.util
import shutil

from contracts import CapabilityReport, CapabilityStatus


class CapabilityDetector:
    def detect(self) -> list[CapabilityReport]:
        adb_status = (
            CapabilityStatus.AVAILABLE
            if shutil.which("adb") is not None
            else CapabilityStatus.UNAVAILABLE
        )
        u2_status = (
            CapabilityStatus.AVAILABLE
            if importlib.util.find_spec("uiautomator2") is not None
            else CapabilityStatus.UNAVAILABLE
        )
        return [
            CapabilityReport(name="android.adb", status=adb_status),
            CapabilityReport(name="android.u2", status=u2_status),
        ]
