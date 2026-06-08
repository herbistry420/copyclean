---
name: copyclean
description: Use when the user wants text or code copied cleanly to the clipboard for pasting into another app (blog post, video description, email, social caption, CMS field, message, code editor), when they say "copy that" / "copy that clean" / "put that on my clipboard", or when they complain about mangled formatting / extra line breaks / spaces after copying from the terminal.
---

# CopyClean

CopyClean puts clean, paste-ready text on the macOS clipboard so the user never
has to mouse-select from the terminal (which bakes in soft-wrap line breaks,
indentation, and extra blank lines). It is **on demand**: the user grabs the last
thing you produced when they want it.

## Why on-demand, not automatic

An earlier version used a sticky flag plus a `Stop` hook. It failed: the hook
fires *before* the final reply is written to the transcript, so it never saw the
block to copy (a timing race). Running on a later user turn avoids this entirely —
by then the message is fully saved. So there is no flag and no hook; the user
triggers the copy.

## How to use it

1. **Fence your deliverables.** Whenever you produce something the user will paste
   elsewhere, put exactly that content in one fenced block. Use a ` ```text `
   fence for prose (write clean plain text — no `**`, `#`, or `-` bullets unless
   they want them literally) and a language fence (` ```swift `, ` ```js `, ...)
   for code (verbatim). Conversational text stays outside the block. This is what
   the copy step grabs.

2. **The user copies it** one of two ways:
   - Types **`/copyclean`** — runs `scripts/copy_last.py`, which finds the most
     recent fenced block in the conversation and pipes its raw text to `pbcopy`.
   - Says **"copy that"** / **"copy that clean"** — do the same yourself: run
     `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/copy_last.py"`, or for a specific
     piece, pipe the exact clean text to `pbcopy` directly.

3. Relay the one-line confirmation; do not reprint the block. The user presses
   **Cmd+V**.

## Important

Tell the user to **paste (Cmd+V), never mouse-select the block in the terminal** —
selecting re-introduces the soft-wrap/indent mangling. The clipboard already holds
the clean version once they run the copy.

## Platform

macOS only (`pbcopy`). The script uses `python3` (present via Xcode / Command Line
Tools).
