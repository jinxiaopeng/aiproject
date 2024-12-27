import logging
import yagmail
from datetime import datetime
from typing import Optional, Dict
import json

class Notifier:
    def __init__(self, config: Optional[Dict] = None):
        self.logger = logging.getLogger(__name__)
        self.config = config or {}
        self._initialize()

    def _initialize(self):
        """初始化通知配置"""
        # 邮件配置
        self.smtp_server = self.config.get('smtp_server', 'smtp.qq.com')
        self.smtp_username = self.config.get('smtp_username', '')
        self.smtp_password = self.config.get('smtp_password', '')
        self.from_email = self.config.get('from_email', '')
        self.admin_emails = self.config.get('admin_emails', [])

        # 初始化邮件客户端
        if self.smtp_username and self.smtp_password:
            try:
                self.yag = yagmail.SMTP(
                    user=self.smtp_username,
                    password=self.smtp_password,
                    host=self.smtp_server
                )
                self.logger.info("邮件客户端初始化成功")
            except Exception as e:
                self.logger.error(f"邮件客户端初始化失败: {str(e)}")
                self.yag = None
        else:
            self.yag = None

        # 通知级别配置
        self.notification_levels = {
            'LOW': ['console'],
            'MEDIUM': ['console', 'email'],
            'HIGH': ['console', 'email'],
            'CRITICAL': ['console', 'email'],
            'WARNING': ['console', 'email']
        }

    def notify(self, threat_event) -> bool:
        """发送威胁事件通知"""
        try:
            level = str(threat_event.level).split('.')[-1]  # 获取枚举值的名称
            channels = self.notification_levels.get(level, ['console'])
            
            message = self._format_message(threat_event)
            
            for channel in channels:
                if channel == 'email':
                    self._send_email(threat_event, message)
                elif channel == 'console':
                    self._log_console(threat_event, message)
            
            return True
        except Exception as e:
            self.logger.error(f"发送通知失败: {str(e)}")
            return False

    def _format_message(self, threat_event) -> str:
        """格式化通知消息"""
        details = json.dumps(threat_event.details, ensure_ascii=False, indent=2) if threat_event.details else "无"
        
        return f"""
威胁事件通知
-------------------
时间: {threat_event.timestamp}
级别: {threat_event.level}
类型: {threat_event.type}
描述: {threat_event.description}
来源IP: {threat_event.source_ip}
状态: {threat_event.status}

详细信息:
{details}
"""

    def _send_email(self, threat_event, message: str):
        """发送邮件通知"""
        if not self.yag or not self.admin_emails:
            self.logger.warning("邮件客户端未初始化或管理员邮箱未配置，跳过邮件通知")
            return

        try:
            subject = f"[威胁告警] {threat_event.type} - {threat_event.level}"
            self.yag.send(
                to=self.admin_emails,
                subject=subject,
                contents=message
            )
            self.logger.info(f"邮件通知已发送至 {', '.join(self.admin_emails)}")
        except Exception as e:
            self.logger.error(f"发送邮件失败: {str(e)}")

    def _log_console(self, threat_event, message: str):
        """输出控制台日志"""
        level = str(threat_event.level).split('.')[-1]
        if level in ['HIGH', 'CRITICAL']:
            self.logger.error(message)
        elif level in ['MEDIUM', 'WARNING']:
            self.logger.warning(message)
        else:
            self.logger.info(message)

    def __del__(self):
        """清理资源"""
        if hasattr(self, 'yag') and self.yag:
            try:
                self.yag.close()
            except:
                pass 