#!/usr/bin/env bash
# Start the WhatsApp bridge and verify connectivity.
# Usage: ./start-whatsapp.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

BRIDGE_URL="${WHATSAPP_BRIDGE_URL:-http://localhost:8081}"

echo "=== WhatsApp MCP — Startup ==="

# 1. Start the bridge container
echo "[1/3] Starting WhatsApp bridge container..."
docker compose up -d whatsapp-bridge

# 2. Wait for the bridge HTTP API to respond
echo "[2/3] Waiting for bridge API at $BRIDGE_URL ..."
MAX_WAIT=30
WAITED=0
while ! curl -so /dev/null -w '' "$BRIDGE_URL/api/send" -X POST -H "Content-Type: application/json" -d '{}' 2>/dev/null; do
    sleep 1
    WAITED=$((WAITED + 1))
    if [ "$WAITED" -ge "$MAX_WAIT" ]; then
        echo "ERROR: Bridge API did not respond within ${MAX_WAIT}s."
        echo "Check logs: docker compose logs whatsapp-bridge"
        exit 1
    fi
done
echo "       Bridge API is up (took ${WAITED}s)."

# 3. Verify SQLite database exists and has data
DB="$SCRIPT_DIR/store/messages.db"
if [ -f "$DB" ]; then
    COUNTS=$(python -c "
import sqlite3, sys
db=sys.argv[1]
c=sqlite3.connect('file:'+db+'?mode=ro', uri=True)
m=c.execute('SELECT count(*) FROM messages').fetchone()[0]
ch=c.execute('SELECT count(*) FROM chats').fetchone()[0]
print(str(m)+' messages, '+str(ch)+' chats')
" "$DB" 2>/dev/null || echo "unknown")
    echo "[3/3] SQLite DB: $COUNTS"
else
    echo "[3/3] WARNING: $DB not found — bridge may need to sync history first."
fi

echo ""
echo "=== WhatsApp MCP ready ==="
echo "Bridge API: $BRIDGE_URL"
echo "MCP server: python src/whatsapp/mcp_server.py"
echo ""
echo "To use in Claude Code, restart your session so .mcp.json is loaded."
