# CopyClean

A small Claude Code plugin that fixes the "I copied text from the terminal and the
formatting went crazy" problem.

When you mouse-select Claude's output in a terminal and paste it into another app
(Google Docs, a CMS, email, a social caption), the terminal bakes in a hard line
break at every soft-wrap point plus stray indentation. CopyClean sidesteps that:
it reads Claude's **raw** output and puts the clean text straight on your clipboard.
You just press **Cmd+V**.

## How it works

Claude puts anything you might paste in a fenced block. CopyClean grabs the most
recent block from the conversation transcript (the clean source, not the wrapped
terminal rendering) and copies it to your clipboard.

It's **on demand** — you trigger the copy when you want it. (An earlier version
auto-copied via a `Stop` hook, but that hook fires before Claude's reply is saved
to the transcript, so it raced and missed the block. Triggering it yourself, after
the reply is on screen, is reliable every time.)

## Triggering a copy — fastest to slowest

1. **Global hotkey** (no typing, no model) — bind `ccopy` to a keyboard shortcut
   (see "Hotkey" below). See a block, press the keys, paste.
2. **`!ccopy`** (no model roundtrip) — type `!ccopy` in the Claude Code prompt;
   the `!` runs it locally and instantly.
3. **`/copyclean:copyclean`** — the plugin command. Goes through a model turn.
4. **"copy that"** — just say it; Claude runs the copier. Also a model turn.

All four call the same `scripts/copy_last.py`.

## Install (one time)

In Claude Code:

```
/plugin marketplace add https://github.com/herbistry420/copyclean
/plugin install copyclean@copyclean
/reload-plugins
```

Then **restart Claude Code once.** On the next session start, the plugin's setup
hook auto-installs the `ccopy` helper on your PATH, so all four triggers — including
the instant `!ccopy` — work immediately. (Commands `/copyclean:copyclean` and "copy
that" work even before the restart.)

> Transparency: CopyClean's only hook is a `SessionStart` setup step that copies a
> small `ccopy` script into a PATH directory (e.g. `/opt/homebrew/bin`). It's
> idempotent and silent. If you'd rather not have a plugin write to your PATH,
> delete `hooks/hooks.json` and run `scripts/install-ccopy.sh` by hand instead.

## Hotkey (optional, macOS — true zero-typing)

1. Open **Shortcuts.app** → New Shortcut.
2. Add the **Run Shell Script** action.
3. Set the script to the full path of `ccopy` (run `command -v ccopy` to find it,
   e.g. `/opt/homebrew/bin/ccopy`).
4. Open the shortcut's info panel → **Add Keyboard Shortcut** → pick a combo that
   doesn't conflict (e.g. `⌃⌥⌘C`).

Now press that combo after Claude shows you a block, then Cmd+V.

## Sharing it

This whole repo is the plugin. A friend installs it with the three commands above
(pointed at this GitHub URL) and a restart. Nothing else to send.

## Requirements

- A clipboard tool: `pbcopy` (macOS, built in), or `wl-copy` / `xclip` / `xsel`
  (Linux), or `clip.exe` (Windows/WSL). The script auto-detects.
- `python3` (built in on macOS with Xcode / Command Line Tools).

> Verified on macOS. The Linux/Windows clipboard backends are wired up but not yet
> tested on those platforms.

## One rule

**Paste (Cmd+V) — don't mouse-select the block in the terminal.** Selecting it
re-introduces the soft-wrap/indent mangling. Once you trigger a copy, the clipboard
already holds the clean version.

## Files

- `commands/copyclean.md` — the `/copyclean` command.
- `skills/copyclean/SKILL.md` — when/how Claude copies; the "copy that" path.
- `scripts/copy_last.py` — finds the latest fenced block and copies it (cross-platform).
- `scripts/install-ccopy.sh` — installs `ccopy` on PATH (idempotent; run by the hook).
- `hooks/hooks.json` — one `SessionStart` setup hook (installs `ccopy`); no copy hook.
- `docs/copyclean-design.md` — design rationale and the race-condition story.
