import asyncio

from hypercorn import Config
from hypercorn.asyncio import serve

from core.server import app

if __name__ == "__main__":
    asyncio.run(serve(app, Config()))
