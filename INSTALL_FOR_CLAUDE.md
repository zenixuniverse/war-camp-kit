# Install instructions for Claude

You are Claude Code. A user gave you this repository's link and asked you to install their camp. Do this for them, start to finish, explaining each step in one plain sentence. Never ask them for a password, token or key: if something needs signing in, they do it themselves in their own terminal or browser.

## 1. Check the basics
- `git --version` and `python --version` (on macOS/Linux try `python3`). Python must be 3.8+.
- If one is missing, tell them exactly what to install (python.org / git-scm.com, or `winget install Python.Python.3.12` / `brew install python`) and wait.

## 2. Get the code
- Pick a permanent home: `~/WarCamp` (Windows: `%USERPROFILE%\WarCamp`). The agents point back to this folder, so it must not be a temp or Downloads folder. Tell them where it's going; use another path only if they ask.
- If the folder already has this repo, `git -C <folder> pull` instead (that's an update; continue to step 3).
- Clone: `git clone <url> <folder>`. The repo is public, so no sign-in is needed. If the clone is refused, the link may point to a private fork: ask them to accept that repo owner's GitHub invitation and sign in once with `gh auth login`, then retry.

## 3. Install
From the camp folder run `python install.py` (or `python3 install.py`). It copies the agents and the camp commands into their Claude Code, wires the live dashboard hook, and backs up anything it replaces. Show them its last lines.

## 4. Start the interview
Run the `/setup-camp` workflow right away: read `<folder>/Machine/Workflows/setup-camp.md` and follow it, treating `<folder>` as the root for every relative path. Tell them the interview takes about 15–20 minutes and they can stop and resume any time with `/setup-camp`.

## 5. Afterwards
- Day to day they can use `/army` from any Claude Code session. For the notes commands (`/today`, `/closeday`, `/meeting-notes`), open Claude Code in the camp folder.
- Updates: `git -C <folder> pull` then `python install.py` again. The interview's answers (BRIEFING, camp.json, orders, their dashboard page) are never overwritten by an update unless the owner changed those same files. If git reports a conflict, keep the user's version and tell them.
