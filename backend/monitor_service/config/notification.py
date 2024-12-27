"""
通知系统配置
"""

# SMTP邮件服务器配置
SMTP_CONFIG = {
    'smtp_server': 'smtp.qq.com',    # QQ邮箱服务器
    'smtp_port': 465,                # QQ邮箱SSL端口
    'smtp_username': '3526357160@qq.com',  # QQ邮箱
    'smtp_password': 'hmvpvaizamnkdaaj',   # QQ邮箱授权码
    'from_email': '3526357160@qq.com',     # 发件人邮箱
    'admin_emails': ['3526357160@qq.com']   # 接收通知的邮箱
}

# 通知级别配置
NOTIFICATION_LEVELS = {
    'LOW': ['console'],                    # 低级别只记录日志
    'MEDIUM': ['console', 'email'],        # 中级别发送邮件
    'HIGH': ['console', 'email'],          # 高级别发送邮件
    'CRITICAL': ['console', 'email'],      # 严重级别发送邮件
    'WARNING': ['console', 'email']        # 警告级别发送邮件
}

# 通知模板配置
NOTIFICATION_TEMPLATES = {
    'email_subject': '[威胁告警] {type} - {level}',
    'email_body': """
威胁事件通知
-------------------
时间: {timestamp}
级别: {level}
类型: {type}
描述: {description}
来源IP: {source_ip}
状态: {status}

详细信息:
{details}
"""
} 