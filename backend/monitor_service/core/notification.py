import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
from ..models.monitor import MonitorAlert
from .config import settings

class NotificationService:
    def __init__(self):
        self.email_config = {
            'smtp_server': settings.SMTP_SERVER,
            'smtp_port': settings.SMTP_PORT,
            'smtp_username': settings.SMTP_USERNAME,
            'smtp_password': settings.SMTP_PASSWORD,
            'sender_email': settings.SENDER_EMAIL
        }
    
    def send_email(self, recipient: str, subject: str, content: str):
        """发送邮件通知"""
        message = MIMEMultipart()
        message['From'] = self.email_config['sender_email']
        message['To'] = recipient
        message['Subject'] = subject
        
        message.attach(MIMEText(content, 'plain'))
        
        try:
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(
                    self.email_config['smtp_username'],
                    self.email_config['smtp_password']
                )
                server.send_message(message)
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            raise
    
    def send_web_notification(self, user_id: int, title: str, content: str):
        """发送Web通知"""
        # TODO: 实现Web Socket通知或其他实时通知机制
        pass
    
    def send_sms(self, phone_number: str, content: str):
        """发送短信通知"""
        # TODO: 实现短信通知
        pass

# 创建通知服务实例
notification_service = NotificationService()

def send_notification(method: str, alert: MonitorAlert, extra_context: Dict[str, Any] = None):
    """发送通知"""
    title = f"[{alert.level}] {alert.title}"
    content = alert.content
    
    if extra_context:
        content += "\n\n附加信息："
        for key, val in extra_context.items():
            content += f"\n{key}: {val}"
    
    try:
        if method == "email":
            # TODO: 从用户配置中获取邮箱地址
            recipient = "user@example.com"
            notification_service.send_email(recipient, title, content)
        elif method == "web":
            notification_service.send_web_notification(alert.user_id, title, content)
        elif method == "sms":
            # TODO: 从用户配置中获取手机号
            phone_number = "1234567890"
            notification_service.send_sms(phone_number, f"{title}\n{content}")
    except Exception as e:
        print(f"Failed to send {method} notification: {str(e)}")
        # 可以选择记录失败的通知到数据库 