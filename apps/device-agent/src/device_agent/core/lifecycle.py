import asyncio


class ShutdownToken:
    def __init__(self) -> None:
        self._event = asyncio.Event()

    def request_shutdown(self) -> None:
        self._event.set()

    @property
    def requested(self) -> bool:
        return self._event.is_set()

    async def wait(self, timeout: float) -> bool:
        try:
            await asyncio.wait_for(self._event.wait(), timeout=timeout)
        except TimeoutError:
            return False
        return True
