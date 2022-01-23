::COPY THIS TO YOUR PROJECT .\lib\
@echo off

echo SCRIPT DISABLED! DELETE THIS 3 LINES
pause
exit

set source="XXX"

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
