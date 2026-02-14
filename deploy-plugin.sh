#!/bin/bash
# deploy-plugin.sh
# Builds pete-pa.zip from the cowork-pa repo ready for drag-and-drop into Cowork.
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
rm -f "$OUTPUT_DIR/$PLUGIN_NAME.plugin.zip"

# Package from the plugin subdirectory
echo "Packaging $PLUGIN_NAME.plugin.zip..."
cd "$PLUGIN_DIR"

if command -v zip &> /dev/null; then
    zip -r "$OUTPUT_DIR/$PLUGIN_NAME.plugin.zip" . \
        -x ".git/*" \
        -x "*.DS_Store"
else
    # Fallback: use PowerShell Compress-Archive on Windows
    echo "zip not found, using PowerShell..."
    WIN_SRC=$(cygpath -w "$PLUGIN_DIR")
    WIN_DST=$(cygpath -w "$OUTPUT_DIR/$PLUGIN_NAME.plugin.zip")
    powershell.exe -NoProfile -Command "Compress-Archive -Path '$WIN_SRC\\*' -DestinationPath '$WIN_DST' -Force"
fi

# Verify the file was created
if [ ! -f "$OUTPUT_DIR/$PLUGIN_NAME.plugin.zip" ]; then
    echo ""
    echo "ERROR: Failed to create $PLUGIN_NAME.plugin.zip"
    exit 1
fi

echo ""
echo "Plugin built: $OUTPUT_DIR/$PLUGIN_NAME.plugin.zip"
echo "Drag and drop into Cowork to install."
