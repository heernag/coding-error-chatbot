@echo off
cd /d D:\1jo_test\frontend
set "PATH=D:\Program Files\nodejs;%PATH%"
call ".\node_modules\.bin\vite.cmd" --host 127.0.0.1 --port 5188 --strictPort
