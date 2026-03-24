@echo off
::  Run the Python script every 2 hours (run this .bat as an administrator)

schtasks /Create  ^
        /SC HOURLY   ^
        /MO 2        ^
        /TN "RunMyPython2Hour" ^
        /TR "\"C:\Python39\python.exe\" \"D:\Code\gmail-notification\main.py\"" ^
        /ST 00:00    ^
        /F

echo Task created (or updated).  Press any key to exit.
pause>nul
