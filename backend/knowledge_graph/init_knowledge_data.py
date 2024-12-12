from datetime import datetime
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models.knowledge import (
    Entity, 
    AttackType, 
    Vulnerability, 
    EntityStatus,
    AttackStatus,
    VulnerabilityStatus,
    VulnerabilitySeverity
)

def init_knowledge_data():
    """初始化知识图谱数据"""
    db = SessionLocal()
    try:
        # 检查是否已有数据
        if db.query(Entity).first():
            print("数据库中已有知识图谱数据，跳过初始化")
            return
            
        # 创建示例知识点
        entities = [
            Entity(
                name="Web安全基础",
                entity_type="concept",
                description="Web安全的基础知识和概念",
                properties={
                    "importance": "high",
                    "estimated_hours": 4
                },
                status=EntityStatus.ACTIVE
            ),
            Entity(
                name="身份认证",
                entity_type="concept",
                description="用户身份验证的原理和方法",
                properties={
                    "importance": "high",
                    "estimated_hours": 3
                },
                status=EntityStatus.ACTIVE
            )
        ]
        db.add_all(entities)
        
        # 创建示例攻击类型
        attacks = [
            AttackType(
                name="SQL注入",
                description="通过在用户输入中注入SQL代码来操纵数据库",
                impact="可能导致数据泄露、数据篡改或数据库破坏",
                mitigation="使用参数化查询，避免直接拼接SQL语句",
                status=AttackStatus.ACTIVE
            ),
            AttackType(
                name="XSS攻击",
                description="跨站脚本攻击，在网页中注入恶意脚本",
                impact="可能窃取用户信息、会话劫持",
                mitigation="对用户输入进行过滤和转义",
                status=AttackStatus.ACTIVE
            )
        ]
        db.add_all(attacks)
        
        # 创建示例漏洞
        vulnerabilities = [
            Vulnerability(
                name="Apache Log4j远程代码执行漏洞",
                cve_id="CVE-2021-44228",
                description="Apache Log4j中的JNDI注入漏洞",
                severity=VulnerabilitySeverity.HIGH,
                affected_systems=["Apache Log4j 2.0-beta9 through 2.15.0"],
                solution="升级到Log4j 2.15.0以上版本",
                status=VulnerabilityStatus.ACTIVE
            ),
            Vulnerability(
                name="Spring4Shell远程代码执行漏洞",
                cve_id="CVE-2022-22965",
                description="Spring Framework中的远程代码执行漏洞",
                severity=VulnerabilitySeverity.HIGH,
                affected_systems=["Spring Framework < 5.3.18", "Spring Framework < 5.2.20"],
                solution="升级到最新版本的Spring Framework",
                status=VulnerabilityStatus.ACTIVE
            )
        ]
        db.add_all(vulnerabilities)
        
        # 提交事务
        db.commit()
        print("知识图谱示例数据创建成功")
        
    except Exception as e:
        print(f"初始化数据时出错: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_knowledge_data() 