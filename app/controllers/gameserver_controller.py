import socket

import a2s

from app.models.form import GameServer


class GameServerController:
    @staticmethod
    async def filter_valid_servers(game_servers: list[GameServer]) -> list[GameServer]:
        for server in [*game_servers]:
            try:
                t = (server.ip, server.port)
                await a2s.ainfo(t)
            except socket.gaierror as e:
                print(type(e).__name__, e)
                game_servers.remove((server))
        return game_servers
