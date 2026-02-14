#!/bin/bash
# deploy-plugin.sh
# Builds pete-pa.plugin from the cowork-pa repo and opens it for Cowork install.
# Usage: ./deploy-plugin.sh [path-to-repo]
# Default repo path: ~/RepoBase/cowork-pa

REPO_DIR="${1:-$HOME/RepoBase/cowork-pa}"
PLUGIN_NAME="pete-pa"
PLUGIN_DIR="$REPO_DIR/$PLUGIN_NAME"
OUTPUT_DIR="$REPO_DIR/dist"

echo "=== Pete PA Plugin Deploy ==="
echo ""

# Check plugin subfolder exists
if [ ! -d "$PLUGIN_DIR/.claude-plugin" ]; then
    echo "ERROR: Plugin not found at $PLUGIN_DIR"
    echo "Expected .claude-plugin directory inside $PLUGIN_DIR"
    echo "Either pass the repo path as an argument or clone it first:"
    echo "  git clone https://github.com/petermcalister/cowork-pa.git $REPO_DIR"
    exit 1
fi

# Pull latest
echo "Pulling latest from origin..."
cd "$REPO_DIR"
git pull origin main
echo ""

# Clean old build
mkdir -p "$OUTPUT_DIR"
rm -f "$OUTPUT_DIR/$PLUGIN_NAME.plugin"

# Package from the plugin subdirectory
echo "Packaging $PLUGIN_NAME.plugin..."
cd "$PLUGIN_DIR"

if command -v zip &> /dev/null; then
    # Use zip if available
    zip -r "$OUTPUT_DIR/$PLUGIN_NAME.plugin" . \
        -x ".git/*" \
        -x "*.DS_Store"
else
    # Fallback: use PowerShell Compress-Archive on Windows
    echo "zip not found, using PowerShell..."
    WIN_SRC=$(cygpath -w "$PLUGIN_DIR")
    WIN_DST=$(cygpath -w "$OUTPUT_DIR/$PLUGIN_NAME.zip")
    WIN_FINAL=$(cygpath -w "$OUTPUT_DIR/$PLUGIN_NAME.plugin")
    powershell.exe -NoProfile -Command "Compress-Archive -Path '$WIN_SRC\\*' -DestinationPath '$WIN_DST' -Force"
    # Rename .zip to .plugin
    mv "$OUTPUT_DIR/$PLUGIN_NAME.zip" "$OUTPUT_DIR/$PLUGIN_NAME.plugin"
fi

# Verify the file was created
if [ ! -f "$OUTPUT_DIR/$PLUGIN_NAME.plugin" ]; then
    echo ""
    echo "ERROR: Failed to create $PLUGIN_NAME.plugin"
    exit 1
fi

echo ""
echo "Plugin built: $OUTPUT_DIR/$PLUGIN_NAME.plugin"
echo ""

# Open the file so Cowork picks it up
echo "Opening plugin file for Cowork install..."
WIN_PLUGIN=$(cygpath -w "$OUTPUT_DIR/$PLUGIN_NAME.plugin" 2>/dev/null)
if [ -n "$WIN_PLUGIN" ]; then
    # Windows (Git Bash / MINGW) — use cmd to open
    cmd.exe //c start "" "$WIN_PLUGIN"
elif command -v open &> /dev/null; then
    open "$OUTPUT_DIR/$PLUGIN_NAME.plugin"
elif command -v xdg-open &> /dev/null; then
    xdg-open "$OUTPUT_DIR/$PLUGIN_NAME.plugin"
else
    echo "Auto-open failed. Drag this file into Cowork: $OUTPUT_DIR/$PLUGIN_NAME.plugin"
fi

echo ""
echo "Done! Accept the plugin in Cowork to complete installation."
