import socket

import a2s
from a2s import GoldSrcInfo, SourceInfo

from app.models.database import ValidGameServer
from app.models.form import GameServer


class GameServerController:
    async def filter_valid_servers(
        self,
        game_servers: list[GameServer],
    ) -> list[ValidGameServer]:
        valid_game_servers: list[ValidGameServer] = []
        game_servers = set(game_servers)

        for server in [*game_servers]:
            try:
                valid_server = await self.get_server_info(server)

                valid_game_servers.append(valid_server)
            except Exception as e:
                game_servers.remove(server)
        return valid_game_servers

    async def get_server_info(self, server: GameServer) -> ValidGameServer:
        hostname = self.to_hostname(server)
        fetched_info: SourceInfo | GoldSrcInfo = await a2s.ainfo(hostname)

        valid_server = ValidGameServer(**self.to_dict(fetched_info))
        valid_server.address = server.address
        valid_server.port = server.port
        return valid_server

    async def get_server_players(self, server: GameServer) -> list[a2s.Player]:
        hostname = self.to_hostname(server)
        fetched_players: list[a2s.Player] = []

        response = await a2s.aplayers(hostname)
        fetched_players.extend(response)

        return fetched_players

    def to_hostname(self, server) -> tuple:
        hostname = (server.address, server.port)
        return hostname

    def to_dict(self, instance: SourceInfo | GoldSrcInfo) -> dict:
        result = {}
        for cls in instance.__class__.__mro__:
            if hasattr(cls, "__slots__"):
                for slot in cls.__slots__:
                    result[slot] = getattr(instance, slot, None)
        return result
