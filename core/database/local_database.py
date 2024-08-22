import uuid
from datetime import datetime, timedelta
from typing import Any

import ezcord


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
            """CREATE TABLE IF NOT EXISTS game_servers (
            server_id INTEGER INTEGER PRIMARY KEY,
            server_name TEXT,
            address TEXT,
            port INTEGER
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

    async def get_setting(
        self, guild_id, feature
    ) -> tuple[None, ...] | Any | tuple | None:
        return await self.one(
            f"SELECT {feature} FROM settings WHERE guild_id=?", guild_id
        )

    async def toggle_setting(self, guild_id, feature) -> None:
        await self.exec(
            "INSERT OR IGNORE INTO settings (guild_id) VALUES (?)", guild_id
        )
        await self.exec(
            f"UPDATE settings SET {feature} = NOT {feature} WHERE guild_id = ?",
            guild_id,
        )


local_db = DashboardDB()
