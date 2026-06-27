from contracts import CapabilityReport, CapabilityStatus, DeviceReport, DeviceStatus


class DeviceDiscovery:
    def __init__(self, *, enable_mock_device: bool = False) -> None:
        self._enable_mock_device = enable_mock_device

    async def discover(self) -> list[DeviceReport]:
        if not self._enable_mock_device:
            return []
        return [
            DeviceReport(
                external_id="mock-device-01",
                name="Mock Android Device",
                status=DeviceStatus.READY,
                capabilities=[
                    CapabilityReport(name="android.adb", status=CapabilityStatus.AVAILABLE),
                    CapabilityReport(name="android.u2", status=CapabilityStatus.AVAILABLE),
                ],
            )
        ]
