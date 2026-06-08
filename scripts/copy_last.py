#!/usr/bin/env python3
"""CopyClean on-demand copier.

Finds the most recent fenced block that the assistant produced in the current
conversation and pipes its raw text to pbcopy. Reads the transcript, so it gets
the clean source (not the terminal's soft-wrapped rendering).

Runs on a fresh user turn (when the user types /copyclean or "copy that"), so the
target message is already fully written to the transcript — no timing race. The
assistant's command-response turn carries no fenced block, so the LAST fence in
the transcript is always the intended deliverable.
"""

import glob
import json
import os
import re
import subprocess
import sys

FENCE_RE = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)

# Clipboard backends in priority order: macOS, Wayland, X11, X11, Windows/WSL.
CLIPBOARD_CMDS = [
    ["pbcopy"],
    ["wl-copy"],
    ["xclip", "-selection", "clipboard"],
    ["xsel", "--clipboard", "--input"],
    ["clip.exe"],
]


def clipboard_copy(text):
    """Copy text to the OS clipboard. Returns the tool used, or None if none work."""
    data = text.encode("utf-8")
    for cmd in CLIPBOARD_CMDS:
        try:
            subprocess.run(cmd, input=data, check=True)
            return cmd[0]
        except (OSError, subprocess.SubprocessError):
            continue
    return None


def _transcript_cwd(path):
    """The working directory recorded in a transcript, or None."""
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except ValueError:
                    continue
                cwd = obj.get("cwd")
                if cwd:
                    return cwd
    except OSError:
        return None
    return None


def newest_transcript():
    """Newest transcript for the CURRENT project (matched by working directory).

    Falls back to the newest transcript overall only when nothing matches the
    current working directory (e.g. run from a global hotkey with no project
    context). This keeps a copy from one project from grabbing a block out of a
    different project's session.
    """
    paths = glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl"))
    if not paths:
        return None
    cwd = os.getcwd()
    scoped = [p for p in paths if _transcript_cwd(p) == cwd]
    pool = scoped if scoped else paths
    return max(pool, key=os.path.getmtime)


def all_assistant_fences(path):
    """Every fenced block from every assistant message, in document order."""
    fences = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except ValueError:
                    continue
                if obj.get("type") != "assistant":
                    continue
                content = obj.get("message", {}).get("content")
                texts = []
                if isinstance(content, list):
                    for b in content:
                        if isinstance(b, dict) and b.get("type") == "text":
                            texts.append(b.get("text", ""))
                elif isinstance(content, str):
                    texts.append(content)
                if texts:
                    fences.extend(FENCE_RE.findall("\n".join(texts)))
    except OSError:
        return []
    return fences


def main():
    path = newest_transcript()
    if not path:
        print("CopyClean: no transcript found.")
        return 1

    fences = all_assistant_fences(path)
    if not fences:
        print("CopyClean: no fenced block found to copy. Ask me to put the text in "
              "a fenced block, then try again.")
        return 1

    body = fences[-1].strip("\n")
    if not body.strip():
        print("CopyClean: the last block was empty.")
        return 1

    tool = clipboard_copy(body)
    if tool is None:
        print("CopyClean: no clipboard tool found. Install one of: pbcopy (macOS), "
              "wl-copy / xclip / xsel (Linux), clip.exe (Windows).")
        return 1

    preview = body[:60].replace("\n", " ")
    print("CopyClean: copied %d chars / ~%d words to the clipboard. Press Cmd+V to "
          "paste. Starts: %r" % (len(body), len(body.split()), preview))
    return 0


if __name__ == "__main__":
    sys.exit(main())
