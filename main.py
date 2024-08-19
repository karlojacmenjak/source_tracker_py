import asyncio
import sys

from app.discord import run_bot
from core.server import run_api


async def main() -> None:
    coros = [run_bot(), run_api()]

    tasks = list(map(asyncio.create_task, coros))
    try:
        await asyncio.gather(*tasks, return_exceptions=True)
    except KeyboardInterrupt:
        for t in tasks:
            t.cancel()
        loop.close()
        print("Program exited")
        sys.exit()


loop = asyncio.get_event_loop()

if __name__ == "__main__":
    loop.run_until_complete(main())
