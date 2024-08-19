import asyncio

from app.discord import run_bot
from core.server import run_api


async def main() -> None:
    loop = asyncio.get_event_loop()
    await asyncio.gather(run_bot(), run_api())


if __name__ == "__main__":
    while True:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
