import uuid
from datetime import datetime, timedelta
from typing import Any

import ezcord

from app.models.database import ValidGameServer
from app.models.form import DashboardSettings, GameServer
from core.factory.controller_factory import ControllerFactory


class DashboardDB(ezcord.DBHandler):
    def __init__(self) -> None:
        super().__init__("dashboard.db")

    async def setup(self) -> None:
        await self.exec(
            """CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT UNIQUE,
            token TEXT,
            refresh_token TEXT,
            token_expires_at TIMESTAMP,
            user_id INTEGER PRIMARY KEY
            )"""
        )

        await self.exec(
            """CREATE TABLE IF NOT EXISTS settings (
            guild_id INTEGER PRIMARY KEY,
            enable_features INTEGER DEFAULT 0,
            check_period INTEGER DEFAULT 60
            )"""
        )

        await self.exec(
            """CREATE TABLE IF NOT EXISTS settings_game_servers (
            guild_id INTEGER,
            server_id INTEGER
            )"""
        )

        await self.exec(
            "CREATE UNIQUE INDEX IF NOT EXISTS guild_game_server ON settings_game_servers (guild_id,server_id)"
        )

        await self.exec(
            """CREATE TABLE IF NOT EXISTS game_servers (
            server_id INTEGER PRIMARY KEY,
            server_name TEXT,
            address TEXT,
            port INTEGER,
            last_data_fetch TIMESTAMP,
            last_response TEXT
            )"""
        )

    async def add_session(self, token, refresh_token, expires_in, user_id) -> str:
        session_id = str(uuid.uuid4())
        expires = datetime.now() + timedelta(seconds=expires_in)

        await self.exec(
            """INSERT OR REPLACE INTO sessions (session_id, token, refresh_token, token_expires_at, user_id)
            VALUES (?, ?, ?, ?, ?)""",
            (session_id, token, refresh_token, expires, user_id),
        )
        return session_id

    async def get_session(self, session_id) -> tuple[None, ...] | Any | tuple | None:
        session = await self.one(
            "SELECT token, refresh_token, token_expires_at FROM sessions WHERE session_id = ?",
            session_id,
            detect_types=1,
        )

        return session

    async def get_user_id(self, session_id) -> Any:
        return await self.one(
            "SELECT user_id FROM sessions WHERE session_id=?", session_id
        )

    async def update_session(
        self, session_id, token, refresh_token, token_expires_at
    ) -> None:
        await self.exec(
            "UPDATE sessions SET token = ?, refresh_token = ?, token_expires_at = ? WHERE session_id = ?",
            (token, refresh_token, token_expires_at, session_id),
            detect_types=1,
        )

    async def delete_session(self, session_id):
        await self.exec("DELETE FROM sessions WHERE session_id = ?", session_id)

    async def add_settings(self, settings: DashboardSettings):
        await self.exec(
            """INSERT OR REPLACE INTO settings (guild_id, enable_features, check_period) VALUES (?, ?, ?)""",
            (settings.guild_id, settings.enable_features, settings.check_period),
        )

    async def exists_settings(self, guild_id: int):
        return await self.one(
            "SELECT EXISTS(SELECT 1 FROM settings WHERE guild_id = ?)", guild_id
        )

    async def get_bot_settings(self, guild_id: int):
        return await self.one(
            "SELECT guild_id, enable_features, check_period FROM settings WHERE guild_id = ?",
            guild_id,
        )

    async def update_game_server_last_fetch(
        self, server: GameServer, valid_server: ValidGameServer
    ) -> None:
        await self.exec(
            "UPDATE game_servers SET last_data_fetch = ?, last_response = ? WHERE address = ? AND port = ?",
            (
                datetime.now(),
                valid_server.model_dump_json(),
                server.address,
                server.port,
            ),
        )

    async def get_game_servers_by_guild(self, guild_id: int) -> list[GameServer]:
        results = await self.all(
            """SELECT address, port, server_name, last_data_fetch, last_response FROM game_servers gs
            LEFT JOIN settings_game_servers sgs ON 
            gs.server_id = sgs.server_id WHERE
            sgs.guild_id = ?
            """,
            (guild_id),
        )

        return [
            GameServer(**{k: v for k, v in zip(GameServer.model_fields.keys(), r)})
            for r in results
        ]

    async def get_game_server(self, server: GameServer) -> GameServer | None:
        result = await self.one(
            """SELECT address, port, server_name, last_data_fetch, last_response FROM game_servers 
            WHERE address = ? AND port = ?
            """,
            (server.address, server.port),
        )
        if not result:
            return None
        return GameServer(
            **{k: v for k, v in zip(GameServer.model_fields.keys(), result)}
        )

    async def update_dashboard_settings(self, settings: DashboardSettings) -> None:
        validator = ControllerFactory.get_gameserver_controller()
        valid_servers = await validator.filter_valid_servers(settings.game_server_list)

        await self.exec(
            "UPDATE settings SET enable_features = ?, check_period = ? WHERE guild_id = ?",
            (settings.enable_features, settings.check_period, settings.guild_id),
            detect_types=1,
        )

        await self.add_game_servers(valid_servers)

        await self.exec(
            "DELETE FROM settings_game_servers WHERE guild_id = ?", (settings.guild_id)
        )

        await self.add_settings_game_servers(settings.guild_id, valid_servers)

    async def add_game_servers(self, valid_servers: ValidGameServer) -> None:
        await self.executemany(
            """
            INSERT OR REPLACE INTO game_servers (server_name, address, port) 
            SELECT ?, ?, ? WHERE NOT EXISTS (
                SELECT * FROM game_servers WHERE address = ? AND port = ?
                )
            """,
            [
                (
                    server.server_name,
                    server.address,
                    server.port,
                    server.address,
                    server.port,
                )
                for server in valid_servers
            ],
        )

    async def add_settings_game_servers(
        self, guild_id: int, valid_servers: list[ValidGameServer]
    ) -> None:
        await self.executemany(
            """INSERT INTO settings_game_servers (guild_id, server_id) 
            SELECT ?, server_id FROM game_servers WHERE address = ? AND port = ?
            ON CONFLICT(guild_id, server_id) DO NOTHING;
            """,
            [(guild_id, server.address, server.port) for server in valid_servers],
        )


local_db = DashboardDB()
