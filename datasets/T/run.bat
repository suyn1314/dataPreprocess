@echo off
set /p str1= ����諸��:
set /p str2= ��אּ:
for /f "delims=" %%i in ('dir /b *.*') do (set "var=%%i" & ren "%%i" "!var:%str1%=%str2!" )