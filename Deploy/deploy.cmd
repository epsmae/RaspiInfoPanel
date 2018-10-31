
@echo off


set OUTPUT_DIRECTORY="Infopanel"


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
copy /y "..\Develop\update_server.txt" %OUTPUT_DIRECTORY%
copy /y "..\Develop\product_name.txt" %OUTPUT_DIRECTORY%
copy /y "..\Develop\infopanel.desktop" %OUTPUT_DIRECTORY%



call powershell.exe -Command "Copy-item -Force -Recurse -Verbose additional_source\* -Destination %OUTPUT_DIRECTORY%"

REM Create zip file with 7zip
"C:\Program Files\7-Zip\7z.exe" a "InfoPanel.zip" ./%OUTPUT_DIRECTORY%


rmdir /S /Q %OUTPUT_DIRECTORY%

pause



