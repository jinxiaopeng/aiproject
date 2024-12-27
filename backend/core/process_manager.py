"""
进程管理模块
"""

import os
import signal
import psutil
import asyncio
import logging
from typing import Dict, Optional
from datetime import datetime

from ..models.challenge import Challenge
from ..services.notification_service import notification_service
from .log_collector import LogCollector
from .environment_manager import EnvironmentManager

logger = logging.getLogger(__name__)

class ProcessManager:
    def __init__(self):
        self.processes: Dict[int, psutil.Process] = {}  # challenge_id -> process
        self.start_times: Dict[int, datetime] = {}      # challenge_id -> start_time
        self._cleanup_task = None
        self.log_collector = LogCollector()
        self.env_manager = EnvironmentManager()

    async def start_process(self, challenge: Challenge) -> Dict:
        """启动靶场进程"""
        if challenge.id in self.processes:
            return self._get_process_status(challenge.id)

        try:
            # 设置靶场环境
            challenge_dir = self.env_manager.setup_challenge(challenge.id)

            # 获取进程配置
            config = challenge.process_config
            if not config:
                raise ValueError("Process configuration not found")

            # 构建命令
            cmd = self._build_command(config)
            env = self.env_manager.prepare_env_vars(challenge.id, config)

            # 启动进程
            process = await asyncio.create_subprocess_exec(
                *cmd,
                env=env,
                cwd=challenge_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                start_new_session=True
            )

            # 记录进程信息
            self.processes[challenge.id] = psutil.Process(process.pid)
            self.start_times[challenge.id] = datetime.utcnow()

            # 更新靶场状态
            challenge.update_status('running')

            # 启动日志收集
            log_file = self.log_collector.start_logging(challenge.id)
            asyncio.create_task(self.log_collector.collect_output(challenge.id, process, "stdout"))
            asyncio.create_task(self.log_collector.collect_output(challenge.id, process, "stderr"))

            # 启动超时检查
            self._start_timeout_check(challenge)

            return self._get_process_status(challenge.id)

        except Exception as e:
            logger.error(f"Failed to start process for challenge {challenge.id}: {str(e)}")
            raise

    async def stop_process(self, challenge_id: int) -> Dict:
        """停止靶场进程"""
        process = self.processes.get(challenge_id)
        if not process:
            return {"status": "stopped"}

        try:
            # 终止进程组
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            process.wait(timeout=5)  # 等待进程终止
        except psutil.TimeoutExpired:
            # 如果进程没有及时终止，强制结束
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        except Exception as e:
            logger.error(f"Error stopping process {challenge_id}: {str(e)}")

        # 停止日志收集
        self.log_collector.stop_logging(challenge_id)

        # 清理环境
        self.env_manager.cleanup_challenge(challenge_id)

        # 清理进程记录
        del self.processes[challenge_id]
        if challenge_id in self.start_times:
            del self.start_times[challenge_id]

        return {"status": "stopped"}

    async def restart_process(self, challenge: Challenge) -> Dict:
        """重启靶场进程"""
        await self.stop_process(challenge.id)
        return await self.start_process(challenge)

    def get_process_status(self, challenge_id: int) -> Optional[Dict]:
        """获取进程状态"""
        if challenge_id not in self.processes:
            return None
        return self._get_process_status(challenge_id)

    def get_process_logs(self, challenge_id: int, lines: int = 100) -> list:
        """获取进程日志"""
        return self.log_collector.get_recent_logs(challenge_id, lines)

    def get_log_file(self, challenge_id: int) -> Optional[str]:
        """获取日志文件路径"""
        return self.log_collector.get_log_file(challenge_id)

    def _get_process_status(self, challenge_id: int) -> Dict:
        """获取进程详细状态"""
        process = self.processes.get(challenge_id)
        if not process:
            return {"status": "stopped"}

        try:
            # 获取进程信息
            with process.oneshot():
                cpu_percent = process.cpu_percent()
                memory_info = process.memory_info()
                memory_percent = process.memory_percent()
                io_counters = process.io_counters()

            # 计算运行时间
            start_time = self.start_times.get(challenge_id)
            run_time = None
            if start_time:
                run_time = (datetime.utcnow() - start_time).total_seconds()

            return {
                "status": "running",
                "pid": process.pid,
                "cpu_percent": cpu_percent,
                "memory_usage": memory_info.rss,
                "memory_percent": memory_percent,
                "io_read_bytes": io_counters.read_bytes,
                "io_write_bytes": io_counters.write_bytes,
                "run_time": run_time
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {"status": "error"}

    def _build_command(self, config: Dict) -> list:
        """构建启动命令"""
        cmd_type = config.get('type', 'python')
        main_file = config.get('main_file')
        if not main_file:
            raise ValueError("Main file not specified")

        if cmd_type == 'python':
            return ['python', main_file]
        elif cmd_type == 'node':
            return ['node', main_file]
        else:
            raise ValueError(f"Unsupported process type: {cmd_type}")

    def _start_timeout_check(self, challenge: Challenge):
        """启动超时检查"""
        if not self._cleanup_task:
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())

    async def _cleanup_loop(self):
        """定期清理超时进程"""
        while True:
            try:
                await self._check_timeouts()
                await asyncio.sleep(60)  # 每分钟检查一次
            except Exception as e:
                logger.error(f"Error in cleanup loop: {str(e)}")

    async def _check_timeouts(self):
        """检查并清理超时进程"""
        now = datetime.utcnow()
        for challenge_id, start_time in list(self.start_times.items()):
            process = self.processes.get(challenge_id)
            if not process:
                continue

            # 获取超时配置
            try:
                challenge = Challenge.get(challenge_id)
                if not challenge:
                    continue

                timeout_config = challenge.timeout_config or {}
                total_timeout = timeout_config.get('total_timeout', 3600)  # 默认1小时
                idle_timeout = timeout_config.get('idle_timeout', 1800)   # 默认30分钟

                # 检查总运行时间
                run_time = (now - start_time).total_seconds()
                if run_time > total_timeout:
                    await self._handle_timeout(challenge_id, "Total timeout exceeded")
                    continue

                # 检查空闲时间
                if idle_timeout:
                    try:
                        cpu_percent = process.cpu_percent()
                        if cpu_percent < 1.0:  # CPU使用率低于1%视为空闲
                            idle_time = (now - process.last_time).total_seconds()
                            if idle_time > idle_timeout:
                                await self._handle_timeout(challenge_id, "Idle timeout exceeded")
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

            except Exception as e:
                logger.error(f"Error checking timeout for challenge {challenge_id}: {str(e)}")

    async def _handle_timeout(self, challenge_id: int, reason: str):
        """处理超时进程"""
        try:
            # 停止进程
            await self.stop_process(challenge_id)

            # 发送通知
            notification_service.send_notification(
                challenge_id,
                "process_timeout",
                {
                    "message": f"Challenge process stopped: {reason}",
                    "challenge_id": challenge_id
                }
            )

        except Exception as e:
            logger.error(f"Error handling timeout for challenge {challenge_id}: {str(e)}")

    def cleanup(self):
        """清理所有进程"""
        for challenge_id in list(self.processes.keys()):
            asyncio.create_task(self.stop_process(challenge_id))

        if self._cleanup_task:
            self._cleanup_task.cancel()

        # 清理旧日志
        self.log_collector.cleanup_old_logs()