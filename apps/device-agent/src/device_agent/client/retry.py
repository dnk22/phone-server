import asyncio
import random
from collections.abc import Awaitable, Callable


async def with_retry[T](
    operation: Callable[[], Awaitable[T]],
    *,
    attempts: int = 3,
    base_delay_seconds: float = 0.05,
) -> T:
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            return await operation()
        except Exception as exc:  # noqa: BLE001 - retry helper maps final exception
            last_error = exc
            if attempt == attempts - 1:
                break
            jitter = random.uniform(0, base_delay_seconds)
            await asyncio.sleep(base_delay_seconds * (2**attempt) + jitter)
    assert last_error is not None
    raise last_error
