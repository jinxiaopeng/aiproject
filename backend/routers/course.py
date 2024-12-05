from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_courses():
    """获取课程列表"""
    return [
        {
            "id": 1,
            "title": "Web安全基础",
            "description": "Web安全基础知识介绍",
            "cover": "https://example.com/course1.jpg",
            "status": "published"
        },
        {
            "id": 2,
            "title": "XSS攻防实战",
            "description": "跨站脚本攻击与防御技术",
            "cover": "https://example.com/course2.jpg",
            "status": "published"
        }
    ]

@router.get("/{course_id}")
async def get_course(course_id: int):
    """获取课程详情"""
    return {
        "id": course_id,
        "title": "Web安全基础",
        "description": "Web安全基础知识介绍",
        "cover": "https://example.com/course1.jpg",
        "status": "published",
        "content": "课程内容..."
    } 