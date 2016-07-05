@echo off
chcp 65001>nul

:: 如果变量没有值的话，内容为空，脚本那个位置的实际也什么都没有
:: 所以可能会有语法错误，引用变量的时候都要在外面加一个包裹
if [%1]==[] (
    set "param=-i"
) else (
    set "param=%1"
)
:: The else needs to be on the same "line" as the if.

:: 调用时未加参数也会报错
if /I [%param%]==[-i] (
title 自动登录IP网关中...
) else (
title 正在退出IP网关...)

:: 工作目录为C:\Windows\System32,%~dp0保存的脚本所在的目录
python "%~dp0ipgw.py" %param% 20144633 Ip.2025642313

pause