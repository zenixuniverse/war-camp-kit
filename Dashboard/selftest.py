#!/usr/bin/env python3
"""Smoke test: start server.py on a free port, hit the GET endpoints, stop it."""
import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def get(port, path):
    with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=5) as r:
        return r.status, r.read().decode("utf-8")


port = free_port()
proc = subprocess.Popen([sys.executable, os.path.join(HERE, "server.py"), "--port", str(port)],
                        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
try:
    for _ in range(50):
        try:
            get(port, "/api/ping")
            break
        except OSError:
            time.sleep(0.1)
    else:
        sys.exit("FAIL: server did not start: " + proc.stderr.read().decode())

    camp = json.loads(get(port, "/api/camp")[1])
    assert camp["businesses"] and camp["theme"]["terms"]["chat"], "camp.json shape"
    for path in ("/api/ping", "/api/army", "/api/army?live=1", "/api/brief", "/api/chat",
                 "/api/live?biz=" + camp["businesses"][0]["id"]):
        status, body = get(port, path)
        assert status == 200, (path, status)
        json.loads(body)
        print("ok  ", path)
    status, html = get(port, "/")
    assert status == 200 and "<script" in html and "/api/camp" in html, "page"
    print("ok   /  (%d bytes)" % len(html))
    try:
        get(port, "/api/live?biz=__nope__")
        sys.exit("FAIL: bad biz accepted")
    except urllib.error.HTTPError as e:
        assert e.code == 400
        print("ok   bad biz -> 400")
    print("SELFTEST PASS")
finally:
    proc.terminate()
    proc.wait(timeout=5)
