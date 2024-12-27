# 邮件通知配置
EMAIL_SETTINGS = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'use_tls': True,
    'username': 'your_email@gmail.com',  # 替换为你的Gmail地址
    'password': 'your_app_password',  # 替换为你的Gmail应用密码
    'from_email': 'your_email@gmail.com',  # 替换为你的Gmail地址
    'admin_emails': ['admin@example.com']  # 替换为接收通知的邮箱地址
}

# 自定义规则配置
CUSTOM_RULES = {
    'suspicious_ports': [22, 23, 3389, 445, 135, 137, 138, 139],  # 扩展可疑端口列表
    'trusted_ips': [
        '192.168.1.1',  # 示例：本地路由器
        '192.168.1.100'  # 示例：可信服务器
    ],
    'blocked_ips': [
        '10.0.0.100',  # 示例：已知恶意IP
        '172.16.0.50'  # 示例：可疑主机
    ]
}

# 开发模式配置
DEBUG = True  # 在开发环境中启用调试模式
TESTING = False

# 性能配置
PERFORMANCE_SETTINGS = {
    'max_packet_processing_threads': 2,  # 减少线程数以适应开发环境
    'max_analysis_threads': 1,
    'queue_size': 500
}

# API配置
API_SETTINGS = {
    'host': 'localhost',  # 仅允许本地访问
    'port': 5000,
    'debug': True,
    'threaded': True
} 