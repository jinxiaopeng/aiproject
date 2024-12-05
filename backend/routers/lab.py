from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_labs():
    """获取实验列表"""
    return [
        {
            "id": 1,
            "title": "SQL注入实验",
            "description": "SQL注入漏洞实验环境",
            "difficulty": "medium",
            "status": "active"
        },
        {
            "id": 2,
            "title": "XSS实验",
            "description": "跨站脚本攻击实验环境",
            "difficulty": "easy",
            "status": "active"
        }
    ]

@router.get("/{lab_id}")
async def get_lab(lab_id: int):
    """获取实验详情"""
    return {
        "id": lab_id,
        "title": "SQL注入实验",
        "description": "SQL注入漏洞实验环境",
        "difficulty": "medium",
        "status": "active",
        "content": "实验内容..."
    } 