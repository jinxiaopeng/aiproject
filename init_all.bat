@echo off
chcp 65001
echo 正在初始化CTF平台数据库...

REM 设置MySQL连接信息
set MYSQL_USER=root
set MYSQL_PASS=jxp1210

REM 初始化主平台数据库
echo 创建主平台数据库...
mysql -u%MYSQL_USER% -p%MYSQL_PASS% < init_platform.sql

REM 初始化SQL注入靶场数据库
echo 创建SQL注入靶场数据库...
mysql -u%MYSQL_USER% -p%MYSQL_PASS% < challenges/sql-injection/init.sql

echo 数据库初始化完成！
pause 