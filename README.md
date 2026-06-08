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
   (see "Fast triggers" below). See a block, press the keys, paste.
2. **`!ccopy`** (no model roundtrip) — type `!ccopy` in the Claude Code prompt;
   the `!` runs it locally and instantly.
3. **`/copyclean:copyclean`** — the plugin command. Goes through a model turn.
4. **"copy that"** — just say it; Claude runs the copier. Also a model turn.

All four call the same `scripts/copy_last.py`.

## Install the plugin (one time)

In Claude Code:

```
/plugin marketplace add <path-or-GitHub-URL-to-this-folder>
/plugin install copyclean@copyclean
/reload-plugins
```

That gives you `/copyclean:copyclean` and the "copy that" behavior.

## Fast triggers (optional, recommended)

These run the copier **without** a model turn.

**Enable `!ccopy`:**

```
bash <this-folder>/scripts/install-ccopy.sh
```

Installs `ccopy` onto your PATH. Then type `!ccopy` in Claude Code anytime.

**Add a global keyboard shortcut (macOS):**

1. Open **Shortcuts.app** → New Shortcut.
2. Add the **Run Shell Script** action.
3. Set the script to the full path of `ccopy` (the installer prints it, e.g.
   `/opt/homebrew/bin/ccopy`).
4. Open the shortcut's info panel → **Add Keyboard Shortcut** → pick a combo that
   doesn't conflict (e.g. `⌃⌥⌘C`).

Now press that combo after Claude shows you a block, then Cmd+V.

## Sharing it with another Claude Code user

This whole folder is the plugin. To share:

- Push it to a Git repo / GitHub, then your friend runs
  `/plugin marketplace add <your-GitHub-URL>` → `/plugin install copyclean@copyclean`.
- Or zip the folder and have them `/plugin marketplace add <unzipped-path>`.

For the fast triggers, they run `scripts/install-ccopy.sh` once and (optionally) set
up their own hotkey.

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
- `scripts/install-ccopy.sh` — installs `ccopy` on your PATH for `!ccopy` + hotkeys.
- `hooks/hooks.json` — intentionally empty (no hooks; see "How it works").
- `docs/copyclean-design.md` — design rationale and the race-condition story.
