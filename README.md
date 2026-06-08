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
the reply is on screen, is reliable every time. CopyClean ships **no hooks**.)

## Use it

Two triggers work the moment you install the plugin — no setup, nothing written to
your system:

- **`/copyclean`** — the command. Copies the latest block.
- **"copy that"** — just say it; Claude runs the copier.

Then press **Cmd+V**.

## Optional: instant `!ccopy` (and a hotkey)

If you want a copy that runs **without** a model turn, install the tiny `ccopy`
helper onto your PATH:

```
bash <plugin-folder>/scripts/install-ccopy.sh
```

(Find `<plugin-folder>` from `/plugin` → Installed, or clone this repo and run it
from there.) After that:

- **`!ccopy`** in the Claude Code prompt runs locally and instantly.
- **Global hotkey (macOS):** Shortcuts.app → New Shortcut → **Run Shell Script** →
  set it to the full path of `ccopy` (run `command -v ccopy` to find it) → add a
  keyboard shortcut in the shortcut's info panel (e.g. `⌃⌥⌘C`).

This step is opt-in by design: the plugin itself never writes to your PATH.

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

## What's in it

- `commands/copyclean.md` — the `/copyclean` command.
- `skills/copyclean/SKILL.md` — when/how Claude copies; the "copy that" path.
- `scripts/copy_last.py` — finds the latest fenced block and copies it (cross-platform).
- `scripts/install-ccopy.sh` — optional: installs the `ccopy` helper on your PATH.
- `docs/copyclean-design.md` — design rationale and the race-condition story.

No hooks, no network access, no third-party dependencies.

## License

MIT — see [LICENSE](LICENSE).

Built by Fordee — [herbistry420.com](https://herbistry420.com).
