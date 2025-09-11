import asyncio
from typing import Callable, Any

async def retry_async(fn: Callable, attempts: int = 3, delay: float = 1.0) -> Any:
    last_err = None
    for i in range(attempts):
        try:
            return await fn()
        except Exception as e:
            last_err = e
            await asyncio.sleep(delay * (2 ** i))
    raise last_err