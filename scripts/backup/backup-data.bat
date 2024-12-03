@echo off
chcp 65001
echo 正在备份数据...

:: 设置备份目录
set BACKUP_DIR=data\backup
set TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_NAME=backup_%TIMESTAMP%

:: 创建备份目录
if not exist %BACKUP_DIR% (
    mkdir %BACKUP_DIR%
)

:: 备份MySQL数据
echo 备份MySQL数据...
mysqldump -u root -pjxp1210 wsirp_db > %BACKUP_DIR%\%BACKUP_NAME%_mysql.sql
if %errorlevel% neq 0 (
    echo [错误] MySQL数据备份失败
) else (
    echo [√] MySQL数据备份成功
)

:: 备份Redis数据
echo 备份Redis数据...
copy data\redis\dump.rdb %BACKUP_DIR%\%BACKUP_NAME%_redis.rdb
if %errorlevel% neq 0 (
    echo [错误] Redis数据备份失败
) else (
    echo [√] Redis数据备份成功
)

:: 备份上传文件
echo 备份上传文件...
xcopy /E /I /Y data\uploads %BACKUP_DIR%\%BACKUP_NAME%_uploads
if %errorlevel% neq 0 (
    echo [错误] 上传文件备份失败
) else (
    echo [√] 上传文件备份成功
)

echo 数据备份完成！
echo 备份文件位置：%BACKUP_DIR%\%BACKUP_NAME%_* 