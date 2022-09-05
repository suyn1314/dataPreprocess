@echo off
set /p str1= 欲更改的值:
set /p str2= 更改為:
for /f "delims=" %%i in ('dir /b *.*') do (set "var=%%i" & ren "%%i" "!var:%str1%=%str2!" )