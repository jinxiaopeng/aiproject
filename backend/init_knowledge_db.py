from sqlalchemy import create_engine
from models.knowledge import Base, KnowledgeNode
from core.config import settings

def init_knowledge_db():
    """初始化知识图谱数据库"""
    print("开始初始化知识图谱数据库...")
    
    # 创建数据库引擎
    engine = create_engine(settings.DATABASE_URL)
    
    # 创建表
    Base.metadata.create_all(engine)
    print("数据库表创建成功")
    
    # 创建一些示例数据
    from sqlalchemy.orm import Session
    with Session(engine) as session:
        # 检查是否已有数据
        if session.query(KnowledgeNode).first():
            print("数据库中已有数据，跳过初始化")
            return
            
        # 创建示例知识点
        nodes = [
            KnowledgeNode(
                name="Web安全基础",
                category="领域",
                difficulty="入门",
                value=10,
                description="Web安全基础知识介绍",
                key_points=["HTTP协议", "Web架构", "安全基础"],
                resources=[{
                    "type": "视频",
                    "items": [{
                        "name": "Web安全入门",
                        "url": "https://example.com/course1"
                    }]
                }]
            ),
            KnowledgeNode(
                name="SQL注入",
                category="漏洞",
                difficulty="进阶",
                value=8,
                description="SQL注入攻击与防御",
                key_points=["SQL基础", "注入原理", "防御方法"],
                resources=[]
            )
        ]
        
        # 添加到数据库
        session.add_all(nodes)
        session.commit()
        print("示例数据创建成功")

if __name__ == "__main__":
    init_knowledge_db() 