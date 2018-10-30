
@echo off


set OUTPUT_DIRECTORY="InfoPanel"

set PWD=%cd%

REM create folder
if not exist %OUTPUT_DIRECTORY% mkdir %OUTPUT_DIRECTORY%

REM delete already existing files in folder
del /Q %OUTPUT_DIRECTORY%\*.*

REM copy files
copy /y "..\Develop\Common.py" %OUTPUT_DIRECTORY%
copy /y "..\Develop\infopanel.py" %OUTPUT_DIRECTORY%
copy /y "..\Develop\printer.py" %OUTPUT_DIRECTORY%
copy /y "..\Develop\usb_updater.py" %OUTPUT_DIRECTORY%
copy /y "..\Develop\web_updater.py" %OUTPUT_DIRECTORY%



call powershell.exe -Command "Copy-item -Force -Recurse -Verbose additional_source\* -Destination %OUTPUT_DIRECTORY%"

REM get version name
REM call powershell.exe -Command "[System.Reflection.Assembly]::LoadFrom('..\..\Develop\VisuTrend.App\bin\Release\VisuTrend.App.exe').GetName().Version.ToString();" > out.tmp
REM set /p VERSION=< out.tmp
REM del /Q out.tmp

REM SET VERSION=%VERSION:.=_%

REM echo Version: %Version%

REM cd %OUTPUT_DIRECTORY%

REM Create zip file with 7zip
"C:\Program Files\7-Zip\7z.exe" a "InfoPanel.zip" ./%OUTPUT_DIRECTORY%

REM cd %PWD%


rmdir /S /Q %OUTPUT_DIRECTORY%

pause



