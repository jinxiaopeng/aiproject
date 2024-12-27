@echo off
echo Building SQL injection challenges...

REM 检查是否已安装所需依赖
python -c "import flask" 2>NUL
if %ERRORLEVEL% NEQ 0 (
    echo Installing Flask...
    pip install flask==2.0.1
)

python -c "import flask_cors" 2>NUL
if %ERRORLEVEL% NEQ 0 (
    echo Installing Flask-CORS...
    pip install flask-cors==3.0.10
)

python -c "import docker" 2>NUL
if %ERRORLEVEL% NEQ 0 (
    echo Installing Docker SDK...
    pip install docker==6.1.2
)

REM 检查Docker镜像是否存在
docker image inspect sql_injection_basic:latest >NUL 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Building basic SQL injection challenge image...
    cd sql_injection
    docker build -t sql_injection_basic:latest .
    cd ..
) else (
    echo Basic SQL injection image already exists.
)

docker image inspect sql_injection_advanced:latest >NUL 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Building advanced SQL injection challenge image...
    cd sql_injection_advanced
    docker build -t sql_injection_advanced:latest .
    cd ..
) else (
    echo Advanced SQL injection image already exists.
)

echo Starting challenge manager...
python challenge_manager.py 