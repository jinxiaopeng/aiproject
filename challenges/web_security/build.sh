#!/bin/bash

# 构建基础SQL注入挑战镜像
cd sql_injection
docker build -t sql_injection_basic:latest .

# 构建进阶SQL注入挑战镜像
cd ../sql_injection_advanced
docker build -t sql_injection_advanced:latest .

# 安装挑战管理器依赖
pip install -r ../requirements.txt

# 启动挑战管理器
python ../challenge_manager.py 