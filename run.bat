@echo off
cd /d "%~dp0"
set DJANGO_SETTINGS_MODULE=settings.development
"venv\Scripts\python.exe" manage.py %*
