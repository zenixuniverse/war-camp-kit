#!/usr/bin/env python3
"""log_event.py - post events to the war camp dashboard and chat.

    python Dashboard/log_event.py "Server restarted"
    python Dashboard/log_event.py -b main -a SCOUT "Proposal sent"
    python Dashboard/log_event.py -a SCOUT --chat-only "Starting the outreach drafts"
    python Dashboard/log_event.py -a SCOUT --chat "Done: drafts in Board/"        # log + chat
    python Dashboard/log_event.py --bump kpis.proposals_sent=2 "Sent 2 proposals"  # bare name = kpis.<name>

-b is a business id from Machine/Army/camp.json (default: the first one).
Posts through the server when it is up; otherwise writes the files directly.
Exit 0 on success, 1 on failure.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import server  # noqa: E402  (same folder; gives us camp.json, paths and the direct-write fallback)

VALID_TYPES = {"ok", "info", "warn", "error"}


def _url():
    return os.environ.get("LOG_SERVER") or f"http://127.0.0.1:{int(server.read_camp().get('dashboard_port') or 5770)}"


def _post(endpoint, payload):
    req = urllib.request.Request(_url() + endpoint, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=3) as r:
            return r.status == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def resolve_biz(biz=None):
    biz = (biz or os.environ.get("LOG_BIZ") or server.biz_ids()[0]).lower()
    if biz not in server.biz_ids():
        sys.exit(f"log_event: unknown business '{biz}' - valid: {', '.join(server.biz_ids())}")
    return biz


def log(msg, agent=None, type="ok", biz=None):
    biz = resolve_biz(biz)
    agent = (agent or os.environ.get("LOG_AGENT") or "").upper()
    if agent:
        msg = f"{agent} · {msg}"
    type = type if type in VALID_TYPES else "info"
    if _post("/api/log", {"biz": biz, "msg": msg, "type": type}):
        return True
    server.do_log(biz, msg, type)  # server down: write the file directly
    return True


def bump(path, by=1, biz=None):
    biz = resolve_biz(biz)
    if "." not in path:
        path = "kpis." + path
    if _post("/api/bump", {"biz": biz, "path": path, "by": by}):
        return True
    server.do_bump(biz, path, by)
    return True


def chat(msg, agent=None):
    agent = (agent or os.environ.get("LOG_AGENT") or "OPERATOR").upper()
    if _post("/api/chat", {"agent": agent, "msg": msg}):
        return True
    server.append_chat(agent, msg)
    return True


def main():
    p = argparse.ArgumentParser(description="Post an event to the war camp dashboard.")
    p.add_argument("msg", nargs="+")
    p.add_argument("-a", "--agent", help="agent nickname / callsign, e.g. SCOUT")
    p.add_argument("-b", "--biz", help="business id from camp.json (default: first)")
    p.add_argument("-t", "--type", default="ok", choices=sorted(VALID_TYPES))
    p.add_argument("--bump", action="append", default=[], metavar="COUNTER[=N]")
    p.add_argument("--chat", action="store_true", help="also post to the chat log")
    p.add_argument("--chat-only", action="store_true", help="chat log only, skip the dashboard feed")
    a = p.parse_args()
    msg = " ".join(a.msg)
    biz = resolve_biz(a.biz)
    try:
        for tok in a.bump:
            name, _, amt = tok.partition("=")
            by = int(amt) if re.fullmatch(r"-?\d+", amt or "") else 1
            bump(name.strip(), by, biz)
            print(f"  bumped [{biz}] {name} += {by}")
        if a.chat or a.chat_only:
            chat(msg, a.agent)
            print(f"  chat <- {(a.agent or 'OPERATOR').upper()}: {msg}")
        if not a.chat_only:
            log(msg, a.agent, a.type, biz)
            print(f"  logged [{biz}/{a.type}] {msg}")
    except (OSError, ValueError) as e:
        print(f"  log_event: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
