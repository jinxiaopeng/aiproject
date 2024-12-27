import os

# 基础配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# 监控配置
MONITORING_INTERVAL = 30  # 监控间隔（秒）
PACKET_BUFFER_SIZE = 1000  # 数据包缓冲区大小
MAX_STORED_THREATS = 1000  # 最大存储威胁数量

# 威胁检测配置
THREAT_PATTERNS = {
    'port_scan': {
        'description': '端口扫描行为',
        'threshold': 20,  # 短时间内扫描端口数量阈值
        'time_window': 60  # 时间窗口（秒）
    },
    'brute_force': {
        'description': '暴力破解尝试',
        'threshold': 10,  # 失败尝试次数阈值
        'time_window': 300  # 时间窗口（秒）
    },
    'ddos': {
        'description': 'DDoS攻击',
        'threshold': 1000,  # 请求数量阈值
        'time_window': 60  # 时间窗口（秒）
    },
    'data_exfiltration': {
        'description': '数据外泄',
        'threshold': 10000000,  # 数据传输量阈值（字节）
        'time_window': 3600  # 时间窗口（秒）
    }
}

# 连接阈值配置
CONNECTION_THRESHOLDS = {
    'max_connections_per_ip': 50,  # 单个IP最大连接数
    'max_internal_connections': 100,  # 内网IP最大连接数
    'high_frequency_threshold': 1000,  # 高频连接阈值
}

# 网络接口配置
NETWORK_INTERFACES = {
    'monitor_all': True,  # 是否监控所有接口
    'excluded_interfaces': [],  # 排除的接口列表
}

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'monitor.log'),
            'formatter': 'standard'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

# 警报配置
ALERT_SETTINGS = {
    'high_threat': {
        'notification_methods': ['log', 'email'],
        'max_alerts_per_hour': 10
    },
    'medium_threat': {
        'notification_methods': ['log'],
        'max_alerts_per_hour': 20
    },
    'low_threat': {
        'notification_methods': ['log'],
        'max_alerts_per_hour': 50
    }
}

# 数据存储配置
STORAGE_SETTINGS = {
    'max_log_size': 10 * 1024 * 1024,  # 最大日志文件大小（字节）
    'max_log_files': 5,  # 最大日志文件数量
    'rotate_logs': True,  # 是否轮转日志
}

# 邮件通知配置
EMAIL_SETTINGS = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'use_tls': True,
    'username': '',  # 需要配置
    'password': '',  # 需要配置
    'from_email': '',  # 需要配置
    'admin_emails': []  # 需要配置
}

# 自定义规则配置
CUSTOM_RULES = {
    'suspicious_ports': [22, 23, 3389],  # 可疑端口列表
    'trusted_ips': [],  # 信任的IP列表
    'blocked_ips': [],  # 阻止的IP列表
}

# API配置
API_SETTINGS = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': False,
    'threaded': True
}

# 性能配置
PERFORMANCE_SETTINGS = {
    'max_packet_processing_threads': 4,
    'max_analysis_threads': 2,
    'queue_size': 1000
}

# 开发模式配置
DEBUG = False
TESTING = False

# 尝试加载本地配置
try:
    from .local_settings import *
except ImportError:
    pass 