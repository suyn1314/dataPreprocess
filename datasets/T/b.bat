@echo off
set /p str1= 欲更改的值:
set /p str2= 更改為:
echo.
echo 請稍後...
for /f "delims=" %%i in ('dir /s /b ^sort /+65535') do (
if "%%~nxa" neq "%~nx0"(
set "file=%%a"
set "name=%%~na"
set "extension=%%~xa"
call set "name=%%name:%str1%=%str2%%%"
setlocal enabledelayedexpansion
ren "!file!" "!name!!extension!" 2>nul
endlocal
)
)
exit