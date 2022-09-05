

@echo off
setlocal enabledelayedexpansion
title 去除指定字符之前或之后的文件名

if "%1"=="" (
@echo 请传参,要删除的字符
@echo "按任意键退出"
pause >nul
exit
)

@echo 将文件名中的[%1]删除掉
@echo --------------------------------------------------
@echo 影响当前目录、子目录带的所有文件,谨慎操作!!!!
@echo --------------------------------------------------
@echo 按Enter键继续，退出直接关闭窗口
pause >nul

for /f "delims=" %%i in ('dir /s /b /a-d ') do (
set m=%%i
set u=!m:%1=!
move "%%i" "!u: =!"
)
@echo ========= 所有目录处理完毕!!!
@echo "按任意键退出"
