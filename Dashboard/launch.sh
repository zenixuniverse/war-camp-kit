#!/bin/sh
# Start the war camp dashboard and open it in the browser.
cd "$(dirname "$0")" || exit 1
PORT=$(python3 -c "import server;print(server.read_camp()['dashboard_port'])" 2>/dev/null || echo 5770)
python3 server.py &
PID=$!
trap 'kill $PID 2>/dev/null' INT TERM EXIT
sleep 2
URL="http://localhost:$PORT"
if command -v open >/dev/null 2>&1; then open "$URL"
elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$URL"
else echo "Open $URL in your browser"; fi
wait $PID
