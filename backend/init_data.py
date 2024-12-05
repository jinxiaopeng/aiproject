from sqlalchemy.orm import Session
from models import Challenge, ChallengeCategory, ChallengeDifficulty
from core.database import get_db

def init_challenges(db: Session):
    """初始化靶场训练题目"""
    challenges = [
        {
            "title": "简单的SQL注入",
            "description": "这是一个简单的SQL注入练习题。尝试通过SQL注入获取管理员的密码。\n\n提示：\n1. 尝试使用单引号闭合\n2. 使用联合查询",
            "category": ChallengeCategory.WEB,
            "difficulty": ChallengeDifficulty.EASY,
            "points": 100,
            "flag": "flag{sql_injection_is_easy}",
            "docker_image": "webgoat/webgoat-8.0",
            "port_mapping": "8080:8080",
            "created_by": 1,
            "is_active": True,
            "is_approved": True
        },
        {
            "title": "XSS漏洞利用",
            "description": "这是一个跨站脚本(XSS)漏洞练习题。尝试通过XSS获取管理员的cookie。\n\n提示：\n1. 尝试在输入框中注入JavaScript代码\n2. 使用alert或console.log测试",
            "category": ChallengeCategory.WEB,
            "difficulty": ChallengeDifficulty.MEDIUM,
            "points": 200,
            "flag": "flag{xss_is_dangerous}",
            "docker_image": "vulnerables/web-dvwa",
            "port_mapping": "80:80",
            "created_by": 1,
            "is_active": True,
            "is_approved": True
        },
        {
            "title": "文件上传漏洞",
            "description": "这是一个文件上传漏洞练习题。尝试绕过文件类型限制上传一个WebShell。\n\n提示：\n1. 尝试修改文件扩展名\n2. 尝试修改Content-Type",
            "category": ChallengeCategory.WEB,
            "difficulty": ChallengeDifficulty.HARD,
            "points": 300,
            "flag": "flag{file_upload_bypass}",
            "docker_image": "vulnerables/upload-vuln",
            "port_mapping": "80:80",
            "created_by": 1,
            "is_active": True,
            "is_approved": True
        }
    ]
    
    for challenge_data in challenges:
        challenge = Challenge(**challenge_data)
        db.add(challenge)
    
    try:
        db.commit()
        print("Successfully initialized challenge data")
    except Exception as e:
        print(f"Failed to initialize challenge data: {e}")
        db.rollback()

if __name__ == "__main__":
    db = next(get_db())
    init_challenges(db) 