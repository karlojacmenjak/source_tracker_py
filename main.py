import asyncio
import sys

from app.discord import run_bot
from core.constant import AppConstants
from core.server import run_api


async def main() -> None:
    coros = [run_bot(), run_api()]

    tasks = list(map(asyncio.create_task, coros))
    try:
        await asyncio.gather(*tasks, return_exceptions=True)
    except KeyboardInterrupt:
        for t in tasks:
            t.cancel()
        print("Program exited")
        sys.exit()


if __name__ == "__main__":
    if AppConstants.production:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    else:
        asyncio.run(main())
