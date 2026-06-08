#!/usr/bin/env bash
# Installs 'ccopy' (the CopyClean on-demand copier) onto your PATH, so you can run
# it instantly as `!ccopy` inside Claude Code, or bind it to a global hotkey.
# One-time setup. Re-run after updating copy_last.py.
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)/copy_last.py"
[ -f "$SRC" ] || { echo "Can't find copy_last.py next to this script."; exit 1; }

DEST=""
for d in /opt/homebrew/bin /usr/local/bin "$HOME/.local/bin" "$HOME/bin"; do
  case ":$PATH:" in
    *":$d:"*) if [ -d "$d" ] && [ -w "$d" ]; then DEST="$d"; break; fi ;;
  esac
done
if [ -z "$DEST" ]; then
  DEST="$HOME/.local/bin"
  mkdir -p "$DEST"
  echo "No writable PATH dir found; using $DEST (add it to your PATH)."
fi

cp "$SRC" "$DEST/ccopy"
chmod +x "$DEST/ccopy"
echo "Installed: $DEST/ccopy"

if command -v ccopy >/dev/null 2>&1; then
  echo "Ready. Type  !ccopy  in Claude Code, or bind  $DEST/ccopy  to a hotkey."
else
  echo "Installed, but $DEST is not on your PATH yet. Add it, then restart your shell."
fi
