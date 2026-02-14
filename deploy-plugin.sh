#!/bin/bash
# deploy-plugin.sh
# Builds pete-pa.plugin from the cowork-pa repo and opens it for Cowork install.
# Usage: ./deploy-plugin.sh [path-to-repo]
# Default repo path: ~/RepoBase/cowork-pa

REPO_DIR="${1:-$HOME/RepoBase/cowork-pa}"
PLUGIN_NAME="pete-pa"
OUTPUT_DIR="$REPO_DIR/dist"

echo "=== Pete PA Plugin Deploy ==="
echo ""

# Check repo exists
if [ ! -d "$REPO_DIR/.claude-plugin" ]; then
    echo "ERROR: Plugin not found at $REPO_DIR"
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

# Package — exclude .git and dist folders
echo "Packaging $PLUGIN_NAME.plugin..."
zip -r "$OUTPUT_DIR/$PLUGIN_NAME.plugin" . \
    -x ".git/*" \
    -x "dist/*" \
    -x "*.DS_Store" \
    -x "deploy-plugin.sh"

echo ""
echo "Plugin built: $OUTPUT_DIR/$PLUGIN_NAME.plugin"
echo ""

# Open the file so Cowork picks it up
echo "Opening plugin file for Cowork install..."
start "$OUTPUT_DIR/$PLUGIN_NAME.plugin" 2>/dev/null \
    || open "$OUTPUT_DIR/$PLUGIN_NAME.plugin" 2>/dev/null \
    || xdg-open "$OUTPUT_DIR/$PLUGIN_NAME.plugin" 2>/dev/null \
    || echo "Auto-open failed. Drag this file into Cowork: $OUTPUT_DIR/$PLUGIN_NAME.plugin"

echo ""
echo "Done! Accept the plugin in Cowork to complete installation."
