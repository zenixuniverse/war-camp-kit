#!/usr/bin/env python3
"""War Camp dashboard server (stdlib only).

Run:  python server.py [--port N]     then open http://localhost:<dashboard_port>

Everything it shows comes from the kit root (parent of Dashboard/):
  Machine/Army/camp.json            names, colours, businesses, terms, port
  Machine/Army/army.json            roster (built by build_army.py)
  Machine/Army/army_live.json       live deployments (written by army_hook.py)
  Machine/Agents/COURT_CHAT.md      the chat log
  Dashboard/data/<biz>_live.json    per-business KPI + activity feed (created on first read)
"""
import http.server
import json
import os
import re
import sys
import threading
import urllib.parse
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE_DIR)
ARMY_DIR = os.path.join(ROOT, "Machine", "Army")
CAMP_FILE = os.path.join(ARMY_DIR, "camp.json")
BRIEF_DIR = os.path.join(ARMY_DIR, "Board", "Daily")
CHAT_FILE = os.path.join(ROOT, "Machine", "Agents", "COURT_CHAT.md")
DATA_DIR = os.path.join(BASE_DIR, "data")
PAGES_DIR = os.path.join(BASE_DIR, "pages")  # each file here is a whole "look"; camp.json theme.page picks one

DEFAULT_CAMP = {
    "org": "Your Company", "army_name": "Your Army", "operator": "Operator",
    "businesses": [{"id": "main", "name": "Your Company", "color": "#d4a04a"}],
    "theme": {"page": "war-camp-3d.html", "camp_title": "War Camp", "accent": "#d4a04a", "accent_2": "#e0463c",
              "background": "#0b0d10", "font_display": "Cinzel",
              "terms": {"army": "Army", "division": "Division", "general": "General",
                        "campaign": "Campaign", "deploy": "Deploy", "chat": "Court Chat"}},
    "dashboard_port": 5770, "timezone": "UTC",
}

MIME = {".html": "text/html; charset=utf-8", ".js": "text/javascript", ".mjs": "text/javascript", ".css": "text/css",
        ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif", ".woff2": "font/woff2",
        ".glb": "model/gltf-binary", ".mp3": "audio/mpeg", ".ico": "image/x-icon"}


def page_file(rel):
    """A file inside Dashboard/pages/, or None (blocks ../ escapes)."""
    full = os.path.normpath(os.path.join(PAGES_DIR, rel.lstrip("/")))
    if not full.startswith(PAGES_DIR + os.sep) or not os.path.isfile(full):
        return None
    return full


def read_camp():
    """camp.json merged over defaults (so a half-filled file never breaks the page)."""
    try:
        with open(CAMP_FILE, encoding="utf-8") as f:
            raw = json.load(f)
    except (OSError, ValueError):
        raw = {}
    camp = {**DEFAULT_CAMP, **{k: v for k, v in raw.items() if not k.startswith("_")}}
    camp["theme"] = {**DEFAULT_CAMP["theme"], **(raw.get("theme") or {})}
    camp["theme"]["terms"] = {**DEFAULT_CAMP["theme"]["terms"], **(raw.get("theme", {}).get("terms") or {})}
    if not camp.get("businesses"):
        camp["businesses"] = DEFAULT_CAMP["businesses"]
    return camp


def now():
    """Local time in camp.json's timezone (falls back to the machine's clock)."""
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo(read_camp().get("timezone") or "UTC"))
    except Exception:
        return datetime.now()


def biz_ids():
    return [b["id"] for b in read_camp()["businesses"]]


def live_path(biz):
    if biz not in biz_ids():
        raise ValueError(f"unknown business '{biz}' (known: {', '.join(biz_ids())})")
    return os.path.join(DATA_DIR, f"{biz}_live.json")


# ── locked JSON read-modify-write ─────────────────────────────────────────
_locks = {}
_locks_guard = threading.Lock()


def _lock_for(path):
    with _locks_guard:
        return _locks.setdefault(path, threading.Lock())


def update_json_file(path, mutate):
    """Atomically read JSON (empty shape if missing), apply mutate(data), stamp, write back."""
    with _lock_for(path):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, ValueError):
            data = {"kpis": {}, "revenue": {}, "log": []}
        mutate(data)
        data["last_updated"] = now().isoformat(timespec="seconds")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return data


def read_live(biz):
    path = live_path(biz)
    if not os.path.exists(path):
        update_json_file(path, lambda d: None)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def do_log(biz, msg, type="info"):
    def mut(d):
        d.setdefault("log", []).insert(0, {"time": now().strftime("%H:%M"), "msg": str(msg), "type": type})
        d["log"] = d["log"][:50]
    update_json_file(live_path(biz), mut)


def do_bump(biz, dotted, by=1):
    out = {}

    def mut(d):
        node = d
        keys = dotted.split(".")
        for k in keys[:-1]:
            if not isinstance(node.get(k), dict):
                node[k] = {}
            node = node[k]
        node[keys[-1]] = (node.get(keys[-1]) or 0) + by
        out["value"] = node[keys[-1]]
    update_json_file(live_path(biz), mut)
    return out["value"]


def do_update(biz, update):
    def mut(d):
        for k, v in update.items():
            if isinstance(v, dict) and isinstance(d.get(k), dict):
                d[k].update(v)
            else:
                d[k] = v
    update_json_file(live_path(biz), mut)


# ── army roster + live deployments ────────────────────────────────────────
_ROSTER = {}


def _load(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def read_army(live_only=False):
    deps = _load(os.path.join(ARMY_DIR, "army_live.json"), {"deployments": []}).get("deployments", [])
    if live_only:
        army = {}
    else:
        path = os.path.join(ARMY_DIR, "army.json")
        try:
            mt = os.path.getmtime(path)
        except OSError:
            mt = 0
        if _ROSTER.get("mt") != mt:  # roster is large and only changes on build_army.py
            _ROSTER["mt"] = mt
            _ROSTER["data"] = _load(path, {"divisions": [], "agents": [], "campaigns": []})
        army = dict(_ROSTER["data"])
    t = datetime.now()
    for d in deps:  # silent 30 min = killed or closed session
        if d.get("status") in ("deployed", "working"):
            try:
                if (t - datetime.fromisoformat(d["updated"])).total_seconds() > 1800:
                    d["status"] = "lost"
            except (KeyError, ValueError):
                pass
    live_st = ("deployed", "working")
    keep = [d for d in deps if d.get("status") in live_st] + [d for d in deps if d.get("status") not in live_st][-40:]
    keep.sort(key=lambda d: d.get("started") or d.get("updated") or "")
    army["deployments"] = [{k: v for k, v in d.items() if k != "brief"} for d in keep]
    army["server_time"] = t.isoformat(timespec="seconds")
    # today's duty results for the first business, written by scheduled musters
    first = biz_ids()[0]
    army["duty_status"] = _load(os.path.join(ARMY_DIR, "rhythm", "status", f"{first}_{t:%Y-%m-%d}.json"), {}).get("duties", {})
    return army


def read_latest_brief():
    try:
        names = sorted(n for n in os.listdir(BRIEF_DIR) if n.endswith("_brief.md"))
    except OSError:
        names = []
    if not names:
        return {"name": None}
    path = os.path.join(BRIEF_DIR, names[-1])
    with open(path, encoding="utf-8") as f:
        md = f.read()
    return {"name": names[-1], "date": names[-1][:10], "markdown": md,
            "mtime": datetime.fromtimestamp(os.path.getmtime(path)).isoformat(timespec="seconds"),
            "path": "Machine/Army/Board/Daily/" + names[-1]}


# ── chat log ──────────────────────────────────────────────────────────────
CHAT_LINE_RE = re.compile(r"^-\s+\[([^\]]+)\]\s+\*\*([A-Za-z0-9-]+):\*\*\s+(.*)$")


def read_chat(limit=120):
    out = []
    try:
        with open(CHAT_FILE, encoding="utf-8") as f:
            for line in f:
                m = CHAT_LINE_RE.match(line.strip())
                if m:
                    out.append({"ts": m.group(1), "agent": m.group(2), "msg": m.group(3)})
    except OSError:
        pass
    return out[-limit:]


def append_chat(agent, msg):
    agent = (agent or "OPERATOR").upper()
    if not re.fullmatch(r"[A-Z0-9][A-Z0-9-]{1,23}", agent):
        agent = "OPERATOR"
    msg = " ".join(str(msg).split())  # one line per message
    if not msg:
        raise ValueError("empty message")
    ts = now().strftime("%Y-%m-%d %H:%M")
    line = f"- [{ts}] **{agent}:** {msg}\n"
    with _lock_for(CHAT_FILE):
        os.makedirs(os.path.dirname(CHAT_FILE), exist_ok=True)
        needs_nl = False
        try:
            with open(CHAT_FILE, "rb") as f:
                f.seek(-1, os.SEEK_END)
                needs_nl = f.read(1) not in (b"\n", b"")
        except OSError:
            pass
        with open(CHAT_FILE, "a", encoding="utf-8") as f:
            f.write(("\n" if needs_nl else "") + line)
    return {"ts": ts, "agent": agent, "msg": msg}


# ── HTTP ──────────────────────────────────────────────────────────────────
class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, mime):
        self.send_response(code)
        self.send_header("Content-Type", mime)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def _biz(self, q, body=None):
        biz = (body or {}).get("biz") or (q.get("biz") or [None])[0] or biz_ids()[0]
        live_path(biz)  # validates
        return biz

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        p = u.path
        try:
            if p in ("/", "/index.html"):
                page = page_file(read_camp()["theme"].get("page") or "") or page_file(DEFAULT_CAMP["theme"]["page"])
                if not page:
                    raise OSError("no page found in Dashboard/pages/")
                with open(page, "rb") as f:
                    self._send(200, f.read(), "text/html; charset=utf-8")
            elif not p.startswith("/api/") and page_file(urllib.parse.unquote(p)):
                full = page_file(urllib.parse.unquote(p))  # a look's own assets (css, js, images, models)
                with open(full, "rb") as f:
                    self._send(200, f.read(), MIME.get(os.path.splitext(full)[1].lower(), "application/octet-stream"))
            elif p == "/api/ping":
                self._json({"status": "ok", "time": now().isoformat(timespec="seconds")})
            elif p == "/api/camp":
                self._json(read_camp())
            elif p == "/api/army":
                self._json(read_army(live_only="live" in q))
            elif p == "/api/brief":
                self._json(read_latest_brief())
            elif p == "/api/chat":
                self._json({"messages": read_chat(), "path": "Machine/Agents/COURT_CHAT.md"})
            elif p == "/api/live":
                self._json(read_live(self._biz(q)))
            else:
                self._send(404, b"not found", "text/plain")
        except ValueError as e:
            self._json({"status": "error", "msg": str(e)}, 400)
        except OSError as e:
            self._json({"status": "error", "msg": str(e)}, 500)

    def do_POST(self):
        p = urllib.parse.urlparse(self.path).path
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            if p == "/api/chat":
                self._json({"status": "ok", "entry": append_chat(body.get("agent"), body.get("msg", ""))})
            elif p == "/api/log":
                do_log(self._biz({}, body), body.get("msg", ""), body.get("type", "info"))
                self._json({"status": "logged"})
            elif p == "/api/bump":
                biz = self._biz({}, body)
                self._json({"status": "ok", "path": body["path"], "value": do_bump(biz, body["path"], body.get("by", 1))})
            elif p == "/api/update":
                do_update(self._biz({}, body), body.get("data") or {})
                self._json({"status": "updated"})
            else:
                self._send(404, b"not found", "text/plain")
        except (ValueError, KeyError, TypeError) as e:
            self._json({"status": "error", "msg": str(e)}, 400)
        except OSError as e:
            self._json({"status": "error", "msg": str(e)}, 500)


def main():
    port = int(read_camp().get("dashboard_port") or 5770)
    if "--port" in sys.argv:
        port = int(sys.argv[sys.argv.index("--port") + 1])
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.daemon_threads = True
    camp = read_camp()
    print(f"\n  {camp['theme']['camp_title']} - {camp['army_name']}")
    print(f"  Running at:  http://localhost:{port}")
    print(f"  Kit root:    {ROOT}")
    print("  Press Ctrl+C to stop\n", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")


if __name__ == "__main__":
    main()
