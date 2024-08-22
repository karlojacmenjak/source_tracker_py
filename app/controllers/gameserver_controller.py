import socket

import a2s
from a2s import GoldSrcInfo, SourceInfo

from app.models.database import ValidGameServers
from app.models.form import GameServer


class GameServerController:
    async def filter_valid_servers(
        self,
        game_servers: list[GameServer],
    ) -> list[ValidGameServers]:
        valid_game_servers: list[ValidGameServers] = []
        game_servers = set(game_servers)

        for server in game_servers:
            try:
                hostname = (server.ip, server.port)
                fetched_info: SourceInfo | GoldSrcInfo = await a2s.ainfo(hostname)

                valid_server = ValidGameServers(**self.to_dict(fetched_info))
                valid_server.address = server.ip
                valid_server.port = server.port

                valid_game_servers.append(valid_server)
            except socket.gaierror as e:
                print(type(e).__name__, e)
                game_servers.remove((server))
        return valid_game_servers

    def to_dict(self, instance: SourceInfo | GoldSrcInfo) -> dict:
        result = {}
        for cls in instance.__class__.__mro__:
            if hasattr(cls, "__slots__"):
                for slot in cls.__slots__:
                    result[slot] = getattr(instance, slot, None)
        return result
