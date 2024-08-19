import asyncio

from app.discord import run_bot
from core.server import run_api


async def main() -> None:
    await asyncio.gather(run_bot(), run_api())


loop = asyncio.get_event_loop()

if __name__ == "__main__":
    while True:
        try:
            loop.run_until_complete(main())
        except KeyboardInterrupt:
            print("Program exited")
            loop.close()
