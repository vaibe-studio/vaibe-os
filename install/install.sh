#!/usr/bin/env bash
# vAIbe-OS installer (base level).
# Downloads the vaibe-os binary from GitHub releases and puts it on PATH.
set -euo pipefail

REPO="vaibe-studio/vaibe-os"
DEST="${VAIBE_OS_HOME:-$HOME/.local/bin}"

mkdir -p "$DEST"

case "$(uname -s)" in
  Linux)  os=linux  ;;
  Darwin) os=darwin ;;
  *) echo "Unsupported OS: $(uname -s). Use install.ps1 on Windows." >&2; exit 1 ;;
esac
case "$(uname -m)" in
  x86_64|amd64)   arch=amd64 ;;
  arm64|aarch64)  arch=arm64 ;;
  *) echo "Unsupported arch: $(uname -m)" >&2; exit 1 ;;
esac

VERSION="${1:-latest}"
if [ "$VERSION" = "latest" ]; then
  VERSION="$(curl -fsSL "https://api.github.com/repos/$REPO/releases/latest" \
    | sed -n 's/.*"tag_name": *"\([^"]*\)".*/\1/p' | head -n1)"
fi
[ -n "$VERSION" ] || { echo "Failed to resolve the latest release" >&2; exit 1; }

ASSET="vaibe-os_${VERSION}_${os}_${arch}.tar.gz"
URL="https://github.com/$REPO/releases/download/$VERSION/$ASSET"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Downloading $URL"
curl -fsSL "$URL" -o "$TMP/vaibe-os.tar.gz"
tar -xzf "$TMP/vaibe-os.tar.gz" -C "$TMP"
install -m 0755 "$TMP/vaibe-os" "$DEST/vaibe-os"

echo "Installed: $DEST/vaibe-os ($VERSION)"
echo "Next: vaibe-os init ~/Projects/my-os"
