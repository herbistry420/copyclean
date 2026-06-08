#!/usr/bin/env bash
# Installs 'ccopy' (the CopyClean on-demand copier) onto your PATH, so you can run
# it instantly as `!ccopy` inside Claude Code, or bind it to a global hotkey.
#
# Idempotent: a no-op once 'ccopy' is present and current. The plugin's
# SessionStart hook runs this with --quiet, so installing the plugin + restarting
# is all your buddy needs. Safe to run by hand too.
set -euo pipefail

QUIET=0
[ "${1:-}" = "--quiet" ] && QUIET=1
say() { [ "$QUIET" -eq 1 ] || echo "$@"; }

SRC="$(cd "$(dirname "$0")" && pwd)/copy_last.py"
[ -f "$SRC" ] || { say "Can't find copy_last.py next to this script."; exit 0; }

# Already installed and identical? Nothing to do.
if command -v ccopy >/dev/null 2>&1 && cmp -s "$SRC" "$(command -v ccopy)"; then
  say "ccopy already up to date ($(command -v ccopy))."
  exit 0
fi

DEST=""
for d in /opt/homebrew/bin /usr/local/bin "$HOME/.local/bin" "$HOME/bin"; do
  case ":$PATH:" in
    *":$d:"*) if [ -d "$d" ] && [ -w "$d" ]; then DEST="$d"; break; fi ;;
  esac
done
if [ -z "$DEST" ]; then
  DEST="$HOME/.local/bin"
  mkdir -p "$DEST"
  say "No writable PATH dir found; using $DEST (add it to your PATH)."
fi

cp "$SRC" "$DEST/ccopy"
chmod +x "$DEST/ccopy"
say "Installed: $DEST/ccopy"
if command -v ccopy >/dev/null 2>&1; then
  say "Ready. Type  !ccopy  in Claude Code, or bind  $DEST/ccopy  to a hotkey."
else
  say "Installed to $DEST, which is not on your PATH yet. Add it, then restart your shell."
fi
