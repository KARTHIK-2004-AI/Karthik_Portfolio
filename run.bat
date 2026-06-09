@echo off
cd /d "c:\Users\YS TECH CENTER\Desktop\Karthik_Portfolio"
set DJANGO_SETTINGS_MODULE=settings.development
"venv\Scripts\python.exe" manage.py %*
