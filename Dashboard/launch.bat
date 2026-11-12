@echo off
rem Start the war camp dashboard and open it in the browser.
cd /d "%~dp0"
set PORT=5770
for /f %%p in ('python -c "import server;print(server.read_camp()['dashboard_port'])" 2^>nul') do set PORT=%%p
start "War Camp server" /min python server.py
timeout /t 2 /nobreak >nul
start "" "http://localhost:%PORT%"
echo War camp running at http://localhost:%PORT% (close the "War Camp server" window to stop it)
