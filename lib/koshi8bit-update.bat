::COPY THIS TO YOUR PROJECT .\lib\
@echo off

set source="C:\k8b\prog\python\lib\lib\koshi8bit"


echo.%source% | findstr %cd% 1>nul

if not errorlevel 1 (
    echo SCRIPT DISABLED! SAME FOLDER
    pause
    exit
)

set dest=%cd%\koshi8bit\
:RESTARTT
rd %dest% /Q /S
IF EXIST %dest% (
	echo ACHTUNG! Folder deletion failed!
    timeout /t 1
    GOTO RESTARTT
)
xcopy %source% %dest% /E /Y
attrib %dest%* /S +R
