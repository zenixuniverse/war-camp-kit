"""Install the camp into this computer's Claude Code.

    python install.py              # install agents + skills, wire the dashboard hook, prime the army
    python install.py --dry-run    # show what would change, touch nothing
    python install.py --home DIR   # install into DIR/.claude instead of ~/.claude (testing)

Safe to re-run. Anything it would overwrite is first copied to ~/.claude/war-camp-backup/<timestamp>/.
Stdlib only, Python 3.8+.
"""
import json, os, re, shutil, subprocess, sys, time
from pathlib import Path

KIT = Path(__file__).resolve().parent
TEXT_EXT = {".md", ".py", ".js", ".mjs", ".json", ".html", ".css", ".txt", ".sh", ".bat", ".yml", ".yaml", ".toml"}
HOOK_EVENTS = ("PreToolUse", "SubagentStart", "SubagentStop")


def main(argv):
    dry = "--dry-run" in argv
    home = Path(argv[argv.index("--home") + 1]).resolve() if "--home" in argv else Path.home()
    claude = home / ".claude"
    agents_dir, skills_dir = claude / "agents", claude / "skills"
    backup = claude / "war-camp-backup" / time.strftime("%Y%m%d-%H%M%S")
    subs = {"{{VAULT}}": KIT.as_posix(), "{{SKILLS}}": skills_dir.as_posix()}
    say = (lambda m: print("[dry-run] " + m)) if dry else print

    def put(src, dst, rel):
        """Copy one file with placeholders filled; back up a different existing file first."""
        data = src.read_bytes()
        if src.suffix.lower() in TEXT_EXT:
            text = data.decode("utf-8")
            for k, v in subs.items():
                text = text.replace(k, v)
            data = text.encode("utf-8")
        if dst.exists():
            old = dst.read_bytes()
            if dst.suffix == ".md":  # ignore the orders block build_army.py adds after install
                old = re.sub(rb"\s*<!-- WAR-CAMP:BEGIN.*?<!-- WAR-CAMP:END -->\s*", b"", old, flags=re.S)
                old = old.replace(b"\r\n", b"\n").rstrip()
                data_cmp = data.replace(b"\r\n", b"\n").rstrip()
            else:
                data_cmp = data
            if old == data_cmp:
                return 0
            if not dry:
                b = backup / rel
                b.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dst, b)
        if not dry:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(data)
        return 1

    # 1. agents
    n = 0
    for sub in ("court", "specialists"):
        for f in sorted((KIT / "agents" / sub).glob("*.md")):
            n += put(f, agents_dir / f.name, Path("agents") / f.name)
    say(f"agents: {n} written to {agents_dir}")

    # 1b. camp commands (/setup-camp, /army) work from any folder
    n = 0
    for f in sorted((KIT / "commands").glob("*.md")):
        n += put(f, claude / "commands" / f.name, Path("commands") / f.name)
    say(f"commands: {n} written to {claude / 'commands'}")

    # 2. skills
    n = 0
    for f in sorted((KIT / "skills").rglob("*")):
        if f.is_file() and "__pycache__" not in f.parts:
            rel = f.relative_to(KIT / "skills")
            n += put(f, skills_dir / rel, Path("skills") / rel)
    say(f"skills: {n} files written to {skills_dir}")

    # 3. dashboard hook in settings.json
    settings_path = claude / "settings.json"
    settings = json.loads(settings_path.read_text(encoding="utf-8")) if settings_path.exists() else {}
    hook_cmd = f'"{Path(sys.executable).as_posix()}" "{(KIT / "Machine" / "Army" / "army_hook.py").as_posix()}"'
    hooks = settings.setdefault("hooks", {})
    added = []
    for ev in HOOK_EVENTS:
        groups = hooks.setdefault(ev, [])
        # drop a stale army_hook entry from an older install location, keep everything else
        for g in groups:
            g["hooks"] = [h for h in g.get("hooks", []) if "army_hook.py" not in h.get("command", "") or h.get("command") == hook_cmd]
        groups[:] = [g for g in groups if g.get("hooks")]
        if not any(h.get("command") == hook_cmd for g in groups for h in g["hooks"]):
            entry = {"hooks": [{"type": "command", "command": hook_cmd, "timeout": 5}]}
            if ev == "PreToolUse":
                entry = {"matcher": "*", **entry}
            groups.append(entry)
            added.append(ev)
    if added and not dry:
        if settings_path.exists():
            backup.mkdir(parents=True, exist_ok=True)
            shutil.copy2(settings_path, backup / "settings.json")
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        settings_path.write_text(json.dumps(settings, indent=2), encoding="utf-8")
    say(f"hook: {'added for ' + ', '.join(added) if added else 'already wired'} in {settings_path}")

    # 4. prime the army with the default (pre-interview) camp
    if dry:
        say("would run Machine/Army/build_army.py")
    else:
        env = dict(os.environ, CAMP_AGENTS_DIR=str(agents_dir))
        r = subprocess.run([sys.executable, str(KIT / "Machine" / "Army" / "build_army.py")], env=env)
        if r.returncode:
            print("build_army.py failed; see the output above.")
            return r.returncode

    if backup.exists():
        print(f"backups of anything replaced: {backup}")
    print("\nDone. Camp folder: %s\nNext: type  /setup-camp  in Claude Code and answer the interview.\n"
          "Dashboard afterwards: Dashboard/launch.bat (Windows) or bash Dashboard/launch.sh" % KIT)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
