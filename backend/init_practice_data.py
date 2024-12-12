from datetime import datetime
from sqlalchemy.orm import Session
from models.lab import Lab
from database import SessionLocal, engine
import json

# 初始化靶场数据
def init_practice_labs():
    db = SessionLocal()
    try:
        # 检查是否已有数据
        if db.query(Lab).count() > 0:
            print("靶场数据已存在，跳过初始化")
            return

        # 初始化靶场数据
        labs = [
            {
                "title": "SQL注入基础训练",
                "description": "通过实践学习SQL注入的基本原理和防御方法",
                "category": "web",
                "difficulty": "easy",
                "points": 100,
                "docker_image": "webgoat/sql-injection:latest",
                "port_mapping": "8080:8080",
                "flag": "flag{sql_injection_basic_done}",
                "hints": ["尝试在登录框中使用特殊字符", "考虑使用单引号闭合SQL语句"],
                "resource_limits": {"cpu": "1", "memory": "512m"},
                "is_active": True
            },
            {
                "title": "XSS跨站脚本攻击",
                "description": "学习XSS攻击的各种类型和防御措施",
                "category": "web",
                "difficulty": "medium",
                "points": 200,
                "docker_image": "webgoat/xss:latest",
                "port_mapping": "8081:8080",
                "flag": "flag{xss_attack_completed}",
                "hints": ["考虑如何绕过基本的XSS过滤", "尝试使用不同的标签和事件处理器"],
                "resource_limits": {"cpu": "1", "memory": "512m"},
                "is_active": True
            },
            {
                "title": "文件上传漏洞利用",
                "description": "探索文件上传漏洞的利用和防御技术",
                "category": "web",
                "difficulty": "hard",
                "points": 300,
                "docker_image": "webgoat/file-upload:latest",
                "port_mapping": "8082:8080",
                "flag": "flag{file_upload_vuln_mastered}",
                "hints": ["检查文件类型验证机制", "考虑绕过前端验证的方法"],
                "resource_limits": {"cpu": "1", "memory": "512m"},
                "is_active": True
            },
            {
                "title": "Linux系统提权",
                "description": "学习Linux系统下的权限提升技术",
                "category": "system",
                "difficulty": "medium",
                "points": 250,
                "docker_image": "vulhub/linux-privilege:latest",
                "port_mapping": "2222:22",
                "flag": "flag{linux_privilege_escalation_done}",
                "hints": ["检查SUID权限的程序", "寻找配置文件中的敏感信息"],
                "resource_limits": {"cpu": "1", "memory": "1g"},
                "is_active": True
            },
            {
                "title": "密码学基础挑战",
                "description": "通过实践了解基本的密码学原理",
                "category": "crypto",
                "difficulty": "easy",
                "points": 150,
                "docker_image": "crypto/basic:latest",
                "port_mapping": "8083:8080",
                "flag": "flag{crypto_basics_completed}",
                "hints": ["观察密文的特征", "考虑常见的加密算法"],
                "resource_limits": {"cpu": "0.5", "memory": "256m"},
                "is_active": True
            }
        ]

        # 添加到数据库
        for lab_data in labs:
            lab = Lab(
                title=lab_data["title"],
                description=lab_data["description"],
                category=lab_data["category"],
                difficulty=lab_data["difficulty"],
                points=lab_data["points"],
                docker_image=lab_data["docker_image"],
                port_mapping=lab_data["port_mapping"],
                flag=lab_data["flag"],
                hints=lab_data["hints"],
                resource_limits=lab_data["resource_limits"],
                is_active=lab_data["is_active"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(lab)

        db.commit()
        print("靶场数据初始化完成")

    except Exception as e:
        print(f"初始化靶场数据失败: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_practice_labs() 