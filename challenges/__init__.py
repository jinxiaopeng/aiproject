"""
Challenge Manager for CTF Platform
"""

import os
import sys
import json
import subprocess
import psutil
import time
from pathlib import Path
import logging
import traceback

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

__all__ = ['ChallengeManager']

class ChallengeManager:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.processes = {}
        self.id_mapping = {
            1: "sql-injection",  # SQL注入基础训练
            2: "xss",           # XSS跨站脚本攻击训练
            3: "file-upload",   # 文件上传漏洞训练
            4: "linux-priv"     # Linux提权训练
        }
        logger.info(f"ChallengeManager initialized with base_path: {self.base_path}")
        logger.debug(f"Available challenges: {list(os.listdir(self.base_path))}")

    def get_challenge_id(self, lab_id):
        """将数字ID转换为字符串ID"""
        logger.debug(f"Converting lab_id: {lab_id} (type: {type(lab_id)})")
        
        # 如果是字符串ID，检查是否是数字字符串
        if isinstance(lab_id, str):
            if lab_id.isdigit():
                lab_id = int(lab_id)
                logger.debug(f"Converted string lab_id to int: {lab_id}")
            else:
                # 如果是字符串ID，检查是否是有效的目录名
                dir_path = self.base_path / lab_id
                logger.debug(f"Checking directory: {dir_path}")
                if dir_path.is_dir():
                    logger.info(f"Found directory for string lab_id: {lab_id}")
                    return lab_id
                logger.warning(f"Directory not found for string lab_id: {lab_id}")
                return None
        
        # 如果是数字ID，尝试从映射中获取
        str_id = self.id_mapping.get(lab_id)
        if str_id:
            logger.info(f"Found mapping for lab_id {lab_id}: {str_id}")
            # 检查目录是否存在
            dir_path = self.base_path / str_id
            logger.debug(f"Checking directory for mapped id: {dir_path}")
            if dir_path.is_dir():
                return str_id
            logger.warning(f"Directory not found for mapped id: {str_id}")
        
        # 如果找不到映射，检查是否有对应的目录
        logger.debug(f"Searching directories for lab_id {lab_id}")
        for dir_name in os.listdir(self.base_path):
            dir_path = self.base_path / dir_name
            if dir_path.is_dir():
                config_path = dir_path / 'config.json'
                logger.debug(f"Checking config file: {config_path}")
                if config_path.exists():
                    try:
                        with open(config_path, 'r', encoding='utf-8') as f:
                            config = json.load(f)
                            logger.debug(f"Config content: {config}")
                            if str(lab_id) == str(config.get('id')):
                                logger.info(f"Found matching config in directory: {dir_name}")
                                return dir_name
                    except Exception as e:
                        logger.error(f"Error reading config file {config_path}: {str(e)}")
                        continue
        logger.warning(f"No matching challenge found for lab_id {lab_id}")
        return None

    def load_challenge_config(self, lab_id):
        challenge_id = self.get_challenge_id(lab_id)
        if not challenge_id:
            raise ValueError(f"Challenge {lab_id} not found")

        config_path = self.base_path / challenge_id / 'config.json'
        logger.info(f"Loading config from: {config_path}")
        if not config_path.exists():
            raise ValueError(f"Challenge {challenge_id} config not found")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            logger.info(f"Loaded config: {config}")
            return config

    def is_port_in_use(self, port):
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            try:
                for conn in proc.connections():
                    if conn.laddr.port == port:
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return False

    def start_challenge(self, lab_id):
        """启动靶场"""
        try:
            logger.info(f"Starting challenge with ID: {lab_id}")
            
            # 获取靶场ID
            challenge_id = self.get_challenge_id(lab_id)
            if not challenge_id:
                raise ValueError(f"Challenge {lab_id} not found")
            
            # 加载配置
            config = self.load_challenge_config(lab_id)
            challenge_port = config['port']
            logger.info(f"Challenge port: {challenge_port}")

            # 检查端口
            if self.is_port_in_use(challenge_port):
                raise RuntimeError(f"Port {challenge_port} is already in use")

            # 准备启动脚本
            src_path = self.base_path / challenge_id / 'src'
            run_script = src_path / 'run.py'
            logger.info(f"Run script path: {run_script}")

            if not run_script.exists():
                raise ValueError(f"Run script not found: {run_script}")

            # 启动进程
            logger.info(f"Starting process with python: {sys.executable}")
            logger.info(f"Working directory: {src_path}")
            
            process = subprocess.Popen(
                [sys.executable, str(run_script), str(challenge_port)],
                cwd=str(src_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            # 等待进程启动
            time.sleep(2)
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                error_msg = f"Process failed to start:\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}"
                logger.error(error_msg)
                raise RuntimeError(error_msg)

            # 保存进程信息
            self.processes[challenge_id] = {
                'process': process,
                'port': challenge_port
            }

            # 启动输出监控线程
            def print_output(process):
                while True:
                    stdout = process.stdout.readline()
                    if stdout:
                        logger.info(f"[{challenge_id}] {stdout.strip()}")
                    stderr = process.stderr.readline()
                    if stderr:
                        logger.error(f"[{challenge_id} ERROR] {stderr.strip()}")
                    if process.poll() is not None:
                        break

            import threading
            output_thread = threading.Thread(target=print_output, args=(process,))
            output_thread.daemon = True
            output_thread.start()

            logger.info(f"Challenge {challenge_id} started successfully")
            return {
                'status': 'running',
                'port': challenge_port,
                'url': f'http://localhost:{challenge_port}'
            }

        except Exception as e:
            error_msg = f"Failed to start challenge: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    def stop_challenge(self, lab_id):
        challenge_id = self.get_challenge_id(lab_id)
        if not challenge_id:
            raise ValueError(f"Challenge {lab_id} not found")

        if challenge_id not in self.processes:
            return {'status': 'not_running'}

        process_info = self.processes[challenge_id]
        process_info['process'].terminate()
        process_info['process'].wait()
        
        # 获取最终输出
        stdout, stderr = process_info['process'].communicate()
        if stdout:
            print(f"Final output from {challenge_id}:\n{stdout}")
        if stderr:
            print(f"Final errors from {challenge_id}:\n{stderr}")
            
        del self.processes[challenge_id]
        return {'status': 'stopped'}

    def get_challenge_status(self, lab_id):
        challenge_id = self.get_challenge_id(lab_id)
        if not challenge_id:
            raise ValueError(f"Challenge {lab_id} not found")

        if challenge_id not in self.processes:
            return {'status': 'not_running'}

        process_info = self.processes[challenge_id]
        if process_info['process'].poll() is None:
            return {
                'status': 'running',
                'port': process_info['port'],
                'url': f'http://localhost:{process_info["port"]}'
            }
        else:
            # 获取最终输出
            stdout, stderr = process_info['process'].communicate()
            if stdout:
                print(f"Final output from {challenge_id}:\n{stdout}")
            if stderr:
                print(f"Final errors from {challenge_id}:\n{stderr}")
            
            del self.processes[challenge_id]
            return {'status': 'stopped'} 