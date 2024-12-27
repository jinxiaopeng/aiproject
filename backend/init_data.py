from sqlalchemy.orm import Session
from backend.models import Challenge
from backend.models.challenge_enums import ChallengeCategory, ChallengeDifficulty
from backend.core.database import get_db

def init_challenges(db: Session):
    """初始化靶场基本信息到主数据库"""
    challenges = [
        {
            "title": "SQL注入基础训练",
            "description": "这是一个简单的SQL注入练习题。尝试通过SQL注入获取管理员的密码。\n\n提示：\n1. 尝试使用单引号闭合\n2. 使用联合查询",
            "category": ChallengeCategory.WEB.value,
            "difficulty": ChallengeDifficulty.EASY.value,
            "points": 100,
            "flag": "flag{sql_injection_is_easy}",
            "process_config": {
                "type": "python",
                "main_file": "challenges/web_security/sql_injection/src/app.py",
                "port": 8080
            },
            "resource_limits": {
                "max_memory": "256M",
                "max_cpu": 50,
                "max_processes": 5
            },
            "timeout_config": {
                "total_timeout": 3600,
                "idle_timeout": 1800,
                "cleanup_interval": 300
            },
            "is_active": True
        },
        {
            "title": "XSS漏洞利用",
            "description": "这是一个跨站脚本(XSS)漏洞练习题。尝试通过XSS获取管理员的cookie。\n\n提示：\n1. 尝试在输入框中注入JavaScript代码\n2. 使用alert或console.log测试",
            "category": ChallengeCategory.WEB.value,
            "difficulty": ChallengeDifficulty.MEDIUM.value,
            "points": 200,
            "flag": "flag{xss_is_dangerous}",
            "process_config": {
                "type": "python",
                "main_file": "challenges/web_security/xss/src/app.py",
                "port": 8081
            },
            "resource_limits": {
                "max_memory": "256M",
                "max_cpu": 50,
                "max_processes": 5
            },
            "timeout_config": {
                "total_timeout": 3600,
                "idle_timeout": 1800,
                "cleanup_interval": 300
            },
            "is_active": True
        },
        {
            "title": "文件上传漏洞",
            "description": "这是一个文件上传漏洞练习题。尝试绕过文件类型限制上传一个WebShell。\n\n提示：\n1. 尝试修改文件扩展名\n2. 尝试修改Content-Type",
            "category": ChallengeCategory.WEB.value,
            "difficulty": ChallengeDifficulty.HARD.value,
            "points": 300,
            "flag": "flag{file_upload_bypass}",
            "process_config": {
                "type": "python",
                "main_file": "challenges/web_security/file_upload/src/app.py",
                "port": 8082
            },
            "resource_limits": {
                "max_memory": "256M",
                "max_cpu": 50,
                "max_processes": 5
            },
            "timeout_config": {
                "total_timeout": 3600,
                "idle_timeout": 1800,
                "cleanup_interval": 300
            },
            "is_active": True
        }
    ]
    
    for challenge_data in challenges:
        challenge = Challenge(**challenge_data)
        db.add(challenge)
    
    try:
        db.commit()
        print("Successfully initialized challenge data in main database")
    except Exception as e:
        print(f"Failed to initialize challenge data: {str(e)}")
        db.rollback()

if __name__ == "__main__":
    db = next(get_db())
    init_challenges(db)