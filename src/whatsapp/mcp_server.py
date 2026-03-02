"""WhatsApp MCP server — stdio transport for Claude Code / Cowork."""

import asyncio
from typing import Optional

from mcp.server.fastmcp import FastMCP

from db import list_chats as db_list_chats
from db import list_messages as db_list_messages
from db import search_contacts as db_search_contacts
from db import get_chat as db_get_chat
import bridge_client

mcp = FastMCP("whatsapp")


# ── Read tools (SQLite direct) ──────────────────────────────────────


@mcp.tool()
def list_chats(
    query: Optional[str] = None,
    limit: int = 20,
    page: int = 0,
    include_last_message: bool = True,
) -> list[dict]:
    """List WhatsApp chats, optionally filtered by name or JID.

    Args:
        query: Search term to match against chat names or JIDs
        limit: Maximum number of chats to return (default 20)
        page: Page number for pagination (default 0)
        include_last_message: Whether to include the last message in each chat
    """
    return db_list_chats(
        query=query,
        limit=limit,
        page=page,
        include_last_message=include_last_message,
    )


@mcp.tool()
def list_messages(
    chat_jid: Optional[str] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
    query: Optional[str] = None,
    sender: Optional[str] = None,
    limit: int = 20,
    page: int = 0,
) -> list[dict]:
    """Get WhatsApp messages with optional filters.

    Args:
        chat_jid: Filter to a specific chat by JID
        after: Only messages after this ISO-8601 timestamp
        before: Only messages before this ISO-8601 timestamp
        query: Search term to filter messages by content
        sender: Filter messages by sender phone number
        limit: Maximum number of messages to return (default 20)
        page: Page number for pagination (default 0)
    """
    return db_list_messages(
        chat_jid=chat_jid,
        after=after,
        before=before,
        query=query,
        sender=sender,
        limit=limit,
        page=page,
    )


@mcp.tool()
def search_contacts(query: str) -> list[dict]:
    """Search WhatsApp contacts by name or phone number.

    Args:
        query: Search term to match against contact names or phone numbers
    """
    return db_search_contacts(query=query)


@mcp.tool()
def get_chat(chat_jid: str, include_last_message: bool = True) -> dict:
    """Get metadata for a specific WhatsApp chat.

    Args:
        chat_jid: The JID of the chat to retrieve
        include_last_message: Whether to include the last message (default True)
    """
    result = db_get_chat(chat_jid=chat_jid, include_last_message=include_last_message)
    if result is None:
        return {"error": f"Chat {chat_jid} not found"}
    return result


# ── Write tools (HTTP → Go bridge) ──────────────────────────────────


@mcp.tool()
async def send_message(recipient: str, message: str) -> dict:
    """Send a WhatsApp text message.

    Args:
        recipient: Phone number (with country code, no +) or JID
                   (e.g. "1234567890" or "1234567890@s.whatsapp.net" or group JID)
        message: The message text to send
    """
    if not recipient:
        return {"success": False, "message": "Recipient is required"}
    if not message:
        return {"success": False, "message": "Message is required"}
    try:
        return await bridge_client.send_message(recipient, message)
    except Exception as e:
        return {"success": False, "message": str(e)}


@mcp.tool()
async def send_file(recipient: str, media_path: str) -> dict:
    """Send a file (image, video, document) via WhatsApp.

    Args:
        recipient: Phone number (with country code, no +) or JID
        media_path: Absolute path to the file to send
    """
    if not recipient:
        return {"success": False, "message": "Recipient is required"}
    if not media_path:
        return {"success": False, "message": "Media path is required"}
    try:
        return await bridge_client.send_file(recipient, media_path)
    except Exception as e:
        return {"success": False, "message": str(e)}


if __name__ == "__main__":
    mcp.run(transport="stdio")
