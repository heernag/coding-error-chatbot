@echo off
cd /d D:\1jo_test
call ".\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000
