"""
日志收集模块
"""

import os
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional
from collections import deque

logger = logging.getLogger(__name__)

class LogCollector:
    def __init__(self, max_lines: int = 1000, log_dir: str = "logs"):
        self.max_lines = max_lines
        self.log_dir = log_dir
        self.log_buffers: Dict[int, deque] = {}  # challenge_id -> log lines
        self.log_files: Dict[int, str] = {}      # challenge_id -> log file path
        
        # 创建日志目录
        os.makedirs(log_dir, exist_ok=True)
    
    def start_logging(self, challenge_id: int) -> str:
        """开始收集日志"""
        # 创建日志缓冲区
        self.log_buffers[challenge_id] = deque(maxlen=self.max_lines)
        
        # 创建日志文件
        log_file = os.path.join(
            self.log_dir,
            f"challenge_{challenge_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        self.log_files[challenge_id] = log_file
        
        return log_file
    
    def stop_logging(self, challenge_id: int):
        """停止收集日志"""
        self.log_buffers.pop(challenge_id, None)
        self.log_files.pop(challenge_id, None)
    
    async def collect_output(
        self,
        challenge_id: int,
        process: asyncio.subprocess.Process,
        output_type: str = "stdout"
    ):
        """收集进程输出"""
        try:
            stream = process.stdout if output_type == "stdout" else process.stderr
            while True:
                line = await stream.readline()
                if not line:
                    break
                    
                # 解码并处理日志行
                log_line = line.decode().strip()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                formatted_line = f"[{timestamp}] [{output_type.upper()}] {log_line}"
                
                # 添加到缓冲区
                if challenge_id in self.log_buffers:
                    self.log_buffers[challenge_id].append(formatted_line)
                
                # 写入文件
                if challenge_id in self.log_files:
                    try:
                        with open(self.log_files[challenge_id], "a") as f:
                            f.write(formatted_line + "\n")
                    except Exception as e:
                        logger.error(f"Error writing to log file: {str(e)}")
                        
        except Exception as e:
            logger.error(f"Error collecting {output_type} for challenge {challenge_id}: {str(e)}")
    
    def get_recent_logs(self, challenge_id: int, lines: int = 100) -> List[str]:
        """获取最近的日志"""
        buffer = self.log_buffers.get(challenge_id)
        if not buffer:
            return []
            
        return list(buffer)[-lines:]
    
    def get_log_file(self, challenge_id: int) -> Optional[str]:
        """获取日志文件路径"""
        return self.log_files.get(challenge_id)
    
    def read_log_file(
        self,
        challenge_id: int,
        start_line: int = 0,
        max_lines: int = 1000
    ) -> List[str]:
        """读取日志文件"""
        log_file = self.get_log_file(challenge_id)
        if not log_file or not os.path.exists(log_file):
            return []
            
        try:
            with open(log_file, "r") as f:
                lines = f.readlines()
                return lines[start_line:start_line + max_lines]
        except Exception as e:
            logger.error(f"Error reading log file: {str(e)}")
            return []
    
    def cleanup_old_logs(self, days: int = 7):
        """清理旧日志文件"""
        try:
            current_time = datetime.now()
            for filename in os.listdir(self.log_dir):
                if not filename.endswith(".log"):
                    continue
                    
                file_path = os.path.join(self.log_dir, filename)
                file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                
                # 删除超过指定天数的日志
                if (current_time - file_time).days > days:
                    try:
                        os.remove(file_path)
                        logger.info(f"Removed old log file: {filename}")
                    except Exception as e:
                        logger.error(f"Error removing log file {filename}: {str(e)}")
                        
        except Exception as e:
            logger.error(f"Error cleaning up old logs: {str(e)}")
    
    def rotate_logs(self, challenge_id: int):
        """轮转日志文件"""
        old_file = self.get_log_file(challenge_id)
        if not old_file:
            return
            
        # 创建新的日志文件
        new_file = os.path.join(
            self.log_dir,
            f"challenge_{challenge_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        
        try:
            # 如果旧文件存在且大小超过限制，进行轮转
            if os.path.exists(old_file) and os.path.getsize(old_file) > 10 * 1024 * 1024:  # 10MB
                self.log_files[challenge_id] = new_file
                logger.info(f"Rotated log file for challenge {challenge_id}")
        except Exception as e:
            logger.error(f"Error rotating log file: {str(e)}") 