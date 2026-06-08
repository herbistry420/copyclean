---
description: Copy the last block of text or code Claude produced to the clipboard, clean
allowed-tools: Bash(python3:*)
---

The user wants the most recent thing you handed them placed on the clipboard,
clean, so they can paste it elsewhere with Cmd+V.

Run exactly this:

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/copy_last.py"`

It finds the most recent fenced block you produced in this conversation, copies
its raw text to the macOS clipboard, and prints a one-line confirmation.

Relay that confirmation line to the user. Do NOT reprint the block itself.
