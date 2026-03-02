"""Read-only SQLite access to the WhatsApp bridge's messages.db."""

import sqlite3
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

# Default path: store/ at the repo root (shared with Docker volume)
DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent.parent / "store" / "messages.db"


@dataclass
class Chat:
    jid: str
    name: Optional[str]
    last_message_time: Optional[str]
    is_group: bool = False
    last_message: Optional[str] = None
    last_sender: Optional[str] = None

    def to_dict(self):
        return asdict(self)


@dataclass
class Message:
    id: str
    chat_jid: str
    sender: str
    content: str
    timestamp: str
    is_from_me: bool
    chat_name: Optional[str] = None
    media_type: Optional[str] = None

    def to_dict(self):
        return asdict(self)


def _connect(db_path: Optional[str] = None) -> sqlite3.Connection:
    path = db_path or str(DEFAULT_DB_PATH)
    return sqlite3.connect(f"file:{path}?mode=ro", uri=True)


def _get_sender_name(cursor: sqlite3.Cursor, sender_jid: str) -> str:
    cursor.execute("SELECT name FROM chats WHERE jid = ? LIMIT 1", (sender_jid,))
    row = cursor.fetchone()
    if row and row[0]:
        return row[0]
    if "@" in sender_jid:
        phone = sender_jid.split("@")[0]
        cursor.execute("SELECT name FROM chats WHERE jid LIKE ? LIMIT 1", (f"%{phone}%",))
        row = cursor.fetchone()
        if row and row[0]:
            return row[0]
    return sender_jid


def list_chats(
    query: Optional[str] = None,
    limit: int = 20,
    page: int = 0,
    include_last_message: bool = True,
    db_path: Optional[str] = None,
) -> list[dict]:
    conn = _connect(db_path)
    try:
        cur = conn.cursor()
        sql = "SELECT c.jid, c.name, c.last_message_time"
        if include_last_message:
            sql += ", m.content, m.sender"
            sql += " FROM chats c LEFT JOIN messages m ON c.jid = m.chat_jid AND c.last_message_time = m.timestamp"
        else:
            sql += " FROM chats c"

        params: list = []
        if query:
            sql += " WHERE (LOWER(c.name) LIKE LOWER(?) OR c.jid LIKE ?)"
            params.extend([f"%{query}%", f"%{query}%"])

        sql += " ORDER BY c.last_message_time DESC LIMIT ? OFFSET ?"
        params.extend([limit, page * limit])

        cur.execute(sql, params)
        rows = cur.fetchall()

        results = []
        for row in rows:
            chat = Chat(
                jid=row[0],
                name=row[1],
                last_message_time=row[2],
                is_group=row[0].endswith("@g.us") if row[0] else False,
                last_message=row[3] if include_last_message and len(row) > 3 else None,
                last_sender=row[4] if include_last_message and len(row) > 4 else None,
            )
            results.append(chat.to_dict())
        return results
    finally:
        conn.close()


def list_messages(
    chat_jid: Optional[str] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
    query: Optional[str] = None,
    sender: Optional[str] = None,
    limit: int = 20,
    page: int = 0,
    db_path: Optional[str] = None,
) -> list[dict]:
    conn = _connect(db_path)
    try:
        cur = conn.cursor()
        sql_parts = [
            "SELECT m.id, m.chat_jid, m.sender, m.content, m.timestamp,",
            "m.is_from_me, c.name, m.media_type",
            "FROM messages m JOIN chats c ON m.chat_jid = c.jid",
        ]
        where: list[str] = []
        params: list = []

        if chat_jid:
            where.append("m.chat_jid = ?")
            params.append(chat_jid)
        if after:
            where.append("m.timestamp > ?")
            params.append(after)
        if before:
            where.append("m.timestamp < ?")
            params.append(before)
        if query:
            where.append("LOWER(m.content) LIKE LOWER(?)")
            params.append(f"%{query}%")
        if sender:
            where.append("m.sender = ?")
            params.append(sender)

        if where:
            sql_parts.append("WHERE " + " AND ".join(where))

        sql_parts.append("ORDER BY m.timestamp DESC LIMIT ? OFFSET ?")
        params.extend([limit, page * limit])

        cur.execute(" ".join(sql_parts), params)
        rows = cur.fetchall()

        results = []
        for row in rows:
            sender_name = _get_sender_name(cur, row[2]) if not row[5] else "Me"
            msg = Message(
                id=row[0],
                chat_jid=row[1],
                sender=sender_name,
                content=row[3] or "",
                timestamp=row[4],
                is_from_me=bool(row[5]),
                chat_name=row[6],
                media_type=row[7],
            )
            results.append(msg.to_dict())
        return results
    finally:
        conn.close()


def search_contacts(
    query: str,
    limit: int = 50,
    db_path: Optional[str] = None,
) -> list[dict]:
    conn = _connect(db_path)
    try:
        cur = conn.cursor()
        pattern = f"%{query}%"
        cur.execute(
            """
            SELECT DISTINCT jid, name FROM chats
            WHERE (LOWER(name) LIKE LOWER(?) OR LOWER(jid) LIKE LOWER(?))
              AND jid NOT LIKE '%@g.us'
            ORDER BY name, jid LIMIT ?
            """,
            (pattern, pattern, limit),
        )
        return [
            {"jid": row[0], "name": row[1], "phone": row[0].split("@")[0]}
            for row in cur.fetchall()
        ]
    finally:
        conn.close()


def get_chat(
    chat_jid: str,
    include_last_message: bool = True,
    db_path: Optional[str] = None,
) -> Optional[dict]:
    conn = _connect(db_path)
    try:
        cur = conn.cursor()
        if include_last_message:
            cur.execute(
                """
                SELECT c.jid, c.name, c.last_message_time, m.content, m.sender
                FROM chats c
                LEFT JOIN messages m ON c.jid = m.chat_jid AND c.last_message_time = m.timestamp
                WHERE c.jid = ?
                """,
                (chat_jid,),
            )
        else:
            cur.execute("SELECT jid, name, last_message_time FROM chats WHERE jid = ?", (chat_jid,))

        row = cur.fetchone()
        if not row:
            return None

        return Chat(
            jid=row[0],
            name=row[1],
            last_message_time=row[2],
            is_group=row[0].endswith("@g.us") if row[0] else False,
            last_message=row[3] if include_last_message and len(row) > 3 else None,
            last_sender=row[4] if include_last_message and len(row) > 4 else None,
        ).to_dict()
    finally:
        conn.close()
