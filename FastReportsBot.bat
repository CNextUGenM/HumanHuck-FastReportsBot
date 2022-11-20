@echo off

call %~dp0FastReportsBot\venv\Scripts\activate

cd %~dp0FastReportsBot

set TOKEN=5609948735:AAF0VPybW--FBeVNhbuBtNeZ4U0LWxfHBsw

python FastReportsBot.py

pause