"""HTTP client for the Go WhatsApp bridge's send/download API."""

import httpx
import os

BRIDGE_URL = os.environ.get("WHATSAPP_BRIDGE_URL", "http://localhost:8080")


async def send_message(recipient: str, message: str) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{BRIDGE_URL}/api/send",
            json={"recipient": recipient, "message": message},
        )
        resp.raise_for_status()
        return resp.json()


async def send_file(recipient: str, media_path: str) -> dict:
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            f"{BRIDGE_URL}/api/send",
            json={"recipient": recipient, "media_path": media_path},
        )
        resp.raise_for_status()
        return resp.json()


async def download_media(message_id: str, chat_jid: str) -> dict:
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            f"{BRIDGE_URL}/api/download",
            json={"message_id": message_id, "chat_jid": chat_jid},
        )
        resp.raise_for_status()
        return resp.json()
