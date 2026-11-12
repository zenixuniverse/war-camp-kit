"""Claude Code hook: records every agent deployment so the Army dashboard shows it live.

Wired in ~/.claude/settings.json for PreToolUse (all tools), SubagentStart and SubagentStop.
- PreToolUse on the Agent tool    -> a new deployment (type + description), status "deployed"
- SubagentStart                   -> links the running agent_id to that deployment, "working"
- PreToolUse inside a subagent    -> updates what it is doing right now ("Edit index.html")
- SubagentStop                    -> "done"
Must never break a session: every failure exits 0 silently.
"""
import json, os, re, sys, time

LIVE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "army_live.json")
LOCK = LIVE + ".lock"
KEEP = 300


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def doing(tool, inp):
    """One short line describing a tool call."""
    inp = inp or {}
    for k in ("description", "file_path", "pattern", "url", "query", "command", "prompt"):
        v = inp.get(k)
        if isinstance(v, str) and v.strip():
            v = v.strip().splitlines()[0]
            if k == "file_path":
                v = os.path.basename(v)
            return f"{tool}: {v[:90]}"
    return tool


def locked(fn):
    # ponytail: spin lock on a lock file; fine for a handful of concurrent hooks
    for _ in range(100):
        try:
            fd = os.open(LOCK, os.O_CREAT | os.O_EXCL)
            break
        except FileExistsError:
            if time.time() - os.path.getmtime(LOCK) > 5:  # stale lock from a killed hook
                os.remove(LOCK)
            time.sleep(0.02)
    else:
        return
    try:
        try:
            with open(LIVE, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, ValueError):
            data = {"deployments": []}
        if fn(data) is not False:
            data["deployments"] = data["deployments"][-KEEP:]
            data["updated"] = now()
            tmp = LIVE + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=1)
            os.replace(tmp, LIVE)
    finally:
        os.close(fd)
        os.remove(LOCK)


def handle(ev):
    name = ev.get("hook_event_name")
    sess = ev.get("session_id", "")
    aid = ev.get("agent_id")
    atype = ev.get("agent_type") or ""

    if name == "PreToolUse" and ev.get("tool_name") in ("Agent", "Task"):
        inp = ev.get("tool_input") or {}
        prompt = inp.get("prompt") or ""
        # /army briefs carry "Campaign: <id>" and "Business: <business id from camp.json>|all" lines
        camp = re.search(r"^Campaign:[ \t]*([a-z0-9-]+)", prompt, re.M)
        biz = re.search(r"^Business:[ \t]*([a-z0-9-]+)", prompt, re.M | re.I)
        def mut(d):
            d["deployments"].append({
                "campaign": camp.group(1) if camp else "",
                "biz": biz.group(1).lower() if biz else "",
                "key": ev.get("tool_use_id") or f"{sess}:{time.time()}",
                "type": inp.get("subagent_type") or "general-purpose",
                "description": inp.get("description", ""),
                "brief": (inp.get("prompt") or "")[:400],
                "by": aid or "CLAUDE",
                "session": sess, "status": "deployed",
                "started": now(), "updated": now(), "doing": "Receiving orders", "actions": 0,
            })
        locked(mut)
        if not aid:
            return

    if name == "SubagentStart" and aid:
        def mut(d):
            for x in reversed(d["deployments"]):
                if x["session"] == sess and x["status"] == "deployed" and not x.get("agent_id") and x["type"] == atype:
                    x.update(agent_id=aid, status="working", updated=now())
                    return
            d["deployments"].append({"key": aid, "agent_id": aid, "type": atype or "agent", "description": "",
                                     "by": "CLAUDE", "session": sess, "status": "working",
                                     "started": now(), "updated": now(), "doing": "Started", "actions": 0})
        locked(mut)
    elif name == "PreToolUse" and aid:
        line = doing(ev.get("tool_name", ""), ev.get("tool_input"))
        def mut(d):
            for x in reversed(d["deployments"]):
                if x.get("agent_id") == aid:
                    x.update(status="working", doing=line, updated=now(), actions=x.get("actions", 0) + 1)
                    return
            # SubagentStart missed: adopt the oldest unlinked deployment of this type
            for x in d["deployments"]:
                if x["session"] == sess and x["status"] == "deployed" and not x.get("agent_id") and x["type"] == atype:
                    x.update(agent_id=aid, status="working", doing=line, updated=now(), actions=1)
                    return
            return False
        locked(mut)
    elif name == "SubagentStop" and aid:
        def mut(d):
            for x in reversed(d["deployments"]):
                if x.get("agent_id") == aid:
                    x.update(status="done", ended=now(), updated=now(), doing="Returned to formation")
                    return
            return False
        locked(mut)


if __name__ == "__main__":
    try:
        raw = sys.stdin.buffer.read().decode("utf-8", "replace")
        ev = json.loads(raw)
        # Fast exit: main-session tool calls that are not dispatches don't concern the army.
        if ev.get("agent_id") or ev.get("tool_name") in ("Agent", "Task") or ev.get("hook_event_name", "").startswith("Subagent"):
            handle(ev)
    except Exception:
        pass
    sys.exit(0)
