# WhatsApp MCP Integration Plan

## Overview

Replace pete-pa's browser-based WhatsApp automation with a local MCP server backed by the whatsmeow Go bridge. The Go bridge runs in Docker Desktop, the Python MCP server runs natively via stdio, and Claude Code/Cowork gets WhatsApp as on-demand tools.

## Architecture

```
Claude Code / Cowork
    │  (stdio — no HTTP)
    ▼
Python MCP Server (native process)
    │  ┌─ SQLite direct reads (store/messages.db)
    │  └─ HTTP POST to localhost:8080 (send/download only)
    ▼
Go WhatsApp Bridge (Docker container)
    │  (whatsmeow / WebSocket)
    ▼
WhatsApp Servers ↔ Pete's Phone
```

**Key constraint:** MCP server must run natively (not in Docker) for stdio transport to work. Only the Go bridge is containerized.

## Feature List

See: `.claude/plans/whatsapp-mcp-features.json`

Total features: 8
Passing: 0

## Files to Create/Modify

| File | Change |
|------|--------|
| `src/whatsapp/bridge/Dockerfile` | Build upstream Go bridge from source |
| `src/whatsapp/bridge/` | Clone/vendor upstream whatsapp-bridge code |
| `src/whatsapp/mcp_server.py` | Python MCP server with stdio transport |
| `src/whatsapp/db.py` | SQLite read layer for messages.db |
| `src/whatsapp/bridge_client.py` | HTTP client for Go bridge send/download API |
| `src/whatsapp/requirements.txt` | Python deps: mcp, httpx |
| `docker-compose.yml` | Go bridge service with store volume |
| `start-whatsapp.sh` | Startup script: bridge + health check |
| `.claude/settings.local.json` | Add whatsapp MCP server config |
| `pete-pa/commands/*.md` | Update allowed-tools to include whatsapp MCP tools |
| `pete-pa/references/browser-whatsapp-guide.md` | Deprecate or redirect to MCP approach |

## Technical Decisions

### Go bridge: fork vs upstream

Clone upstream `lharries/whatsapp-mcp` whatsapp-bridge into `src/whatsapp/bridge/`. No code changes needed — we use the bridge as-is (HTTP API + SQLite). The webhook addition from the architecture doc is deferred (not needed for MCP approach).

### SQLite shared access

The Go bridge writes to `store/messages.db`. The Python MCP server reads it directly with `?mode=ro` (read-only). SQLite WAL mode handles concurrent read/write across processes. The `store/` directory is mounted as a Docker volume and also accessible from the host filesystem.

### MCP tools (matching upstream)

| Tool | Method | Data Source |
|------|--------|-------------|
| `list_chats` | Read | SQLite direct |
| `list_messages` | Read | SQLite direct |
| `search_contacts` | Read | SQLite direct |
| `get_chat` | Read | SQLite direct |
| `send_message` | Write | HTTP → Go bridge |
| `send_file` | Write | HTTP → Go bridge |

Simplified from upstream's 12 tools to 6 — we can add more later.

### QR auth flow

First run requires Pete's attention:
1. `docker compose run --rm whatsapp-bridge` (interactive, shows QR in terminal)
2. Pete scans QR with phone
3. Session persists in `store/whatsapp.db`
4. Subsequent runs: `docker compose up -d whatsapp-bridge` (auto-reconnects)

### Python dependencies

```
mcp[cli]>=1.6.0    # FastMCP framework with stdio transport
httpx>=0.28.0       # Async HTTP for bridge API calls
```

No uv — use pip/venv since uv isn't installed.

## Incremental Order

1. **F001** — Go bridge Dockerfile + docker-compose (blocking — everything depends on the bridge)
2. **F002** — QR auth flow (requires Pete's phone — do early)
3. **F003** — Python MCP server scaffolding (can start before F002 using test data)
4. **F004** — MCP read tools (depends on F003, testable with any messages.db)
5. **F005** — MCP send tools (depends on F001+F002 for live testing)
6. **F006** — Claude Code integration (depends on F003+F004)
7. **F007** — Cowork plugin integration (depends on F006)
8. **F008** — Startup script (final polish, depends on all above)

## Risk: Go compilation on Windows

The upstream bridge uses `mattn/go-sqlite3` which requires CGO + a C compiler. Building inside Docker (golang:1.22-alpine + gcc) avoids this entirely — no Go or C compiler needed on the host.

## Acceptance Criteria

All features in `whatsapp-mcp-features.json` have `passes: true`.
