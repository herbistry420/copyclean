# CopyClean — design

**Date:** 2026-06-08
**Owner:** Fordee
**Status:** Working (on-demand copy shipped and confirmed on macOS)

## Problem

When Claude Code prints text to copy/paste, copying it with the mouse captures the
terminal's *rendered* version: a hard newline at every soft-wrap point, plus
markdown indentation and extra blank lines. Pasting into another app (CMS, Google
Docs, email, social) then needs manual cleanup every time.

## Key insight

The mangling happens at mouse-copy time in the terminal, not in Claude's output.
Claude's *raw* output of a paragraph is already a single clean line. So the fix is:
never copy from the terminal. Read the raw transcript and put the clean text on the
clipboard programmatically; the user just presses Cmd+V.

## Design: on demand

The user triggers the copy when they want it. A small script (`scripts/copy_last.py`)
finds the newest session transcript, collects every fenced block the assistant
produced, and copies the **last** one to the clipboard.

**Triggers (all call the same script):**
- `!ccopy` in the Claude Code prompt — runs locally, no model turn. Fastest typed
  path. Requires `ccopy` on PATH (installed by `scripts/install-ccopy.sh`).
- A macOS global hotkey bound to `ccopy` via Shortcuts.app — zero typing, no model.
- `/copyclean:copyclean` command, or saying "copy that" — both go through a model
  turn (slower; convenient when already chatting).

## Why on-demand and not an automatic hook

The first design used a sticky `/copyclean on` flag plus a `Stop` hook that
auto-copied the last fenced block. It failed in practice: **the `Stop` hook fires
before Claude's final reply is written to the transcript** (a timing race), so it
never saw the block it was meant to copy — the clipboard kept its old contents.
Triggering the copy on a *later* user turn sidesteps the race entirely, because by
then the message is fully saved. So there is no flag and no copy hook. (The plugin
ships exactly one hook — a `SessionStart` setup step that auto-installs the `ccopy`
helper on PATH so `!ccopy` works after install + restart. It does no copying.)

## Components

```
ClaudeCopy/
  .claude-plugin/plugin.json        # manifest
  .claude-plugin/marketplace.json   # local/GitHub install (source ".")
  commands/copyclean.md             # /copyclean -> runs copy_last.py
  skills/copyclean/SKILL.md         # fence-the-deliverable convention + "copy that"
  scripts/copy_last.py              # find newest transcript, copy last fenced block
  scripts/install-ccopy.sh          # install `ccopy` on PATH (idempotent, --quiet)
  hooks/hooks.json                  # one SessionStart setup hook (installs ccopy)
  README.md                         # install, triggers, sharing
  docs/copyclean-design.md          # this file
```

## Clipboard portability

`copy_last.py` auto-detects a clipboard backend: `pbcopy` (macOS), `wl-copy` /
`xclip` / `xsel` (Linux), `clip.exe` (Windows/WSL). Verified on macOS; the other
backends are wired but untested.

## Convention

Claude puts each pasteable deliverable in exactly one fenced block (` ```text ` for
prose written as clean plain text, a language fence for code kept verbatim), with
conversational text outside the block. The copier grabs the most recent block.

## Out of scope (v1)

- Rich-text / RTF clipboard (markdown → bold/headings). Plain text + verbatim code.
- Cleaning arbitrary clipboard contents from other tools.
- Auto-copy without a user trigger (abandoned — the Stop-hook race above).
