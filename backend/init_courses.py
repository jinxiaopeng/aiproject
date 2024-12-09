from sqlalchemy.orm import Session
from models.course import Course, Chapter
from core.database import get_db, engine, Base
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_courses(db: Session):
    """初始化课程数据"""
    try:
        # 检查是否已存在课程
        existing_course = db.query(Course).first()
        if existing_course:
            logger.info("课程数据已存在")
            return

        logger.info("开始创建课程数据...")
        # 示例课程数据
        courses_data = [
            {
                "title": "Web安全基础入门",
                "description": "本课程介绍Web安全的基本概念和常见漏洞类型，帮助初学者建立安全意识。",
                "cover_url": "/images/courses/web-security-basic.jpg",
                "category": "web_security",
                "difficulty": "beginner",
                "instructor_id": 1,  # admin用户
                "chapters": [
                    {
                        "title": "Web安全概述",
                        "description": "介绍Web安全的重要性和基本概念",
                        "order": 1,
                        "duration": 30,
                        "video_url": "/videos/web-security/chapter1.mp4"
                    },
                    {
                        "title": "常见Web漏洞类型",
                        "description": "详解OWASP Top 10安全风险",
                        "order": 2,
                        "duration": 45,
                        "video_url": "/videos/web-security/chapter2.mp4"
                    }
                ]
            },
            {
                "title": "渗透测试实战",
                "description": "通过实际案例学习渗透测试方法和工具的使用。",
                "cover_url": "/images/courses/pentest-practice.jpg",
                "category": "penetration_testing",
                "difficulty": "intermediate",
                "instructor_id": 1,
                "chapters": [
                    {
                        "title": "渗透测试方法论",
                        "description": "介绍渗透测试的基本流程和方法",
                        "order": 1,
                        "duration": 40,
                        "video_url": "/videos/pentest/chapter1.mp4"
                    },
                    {
                        "title": "信息收集技术",
                        "description": "学习目标系统信息收集的各种方法",
                        "order": 2,
                        "duration": 50,
                        "video_url": "/videos/pentest/chapter2.mp4"
                    }
                ]
            },
            {
                "title": "网络安全防护",
                "description": "学习网络安全防护的基本原理和实践方法。",
                "cover_url": "/images/courses/network-security.jpg",
                "category": "network_security",
                "difficulty": "intermediate",
                "instructor_id": 1,
                "chapters": [
                    {
                        "title": "网络安全基础",
                        "description": "介绍网络安全的基本概念和原理",
                        "order": 1,
                        "duration": 35,
                        "video_url": "/videos/network/chapter1.mp4"
                    },
                    {
                        "title": "防火墙配置",
                        "description": "学习防火墙的配置和管理",
                        "order": 2,
                        "duration": 55,
                        "video_url": "/videos/network/chapter2.mp4"
                    }
                ]
            }
        ]

        # 添加课程和章节
        for course_data in courses_data:
            logger.info(f"创建课程: {course_data['title']}")
            chapters = course_data.pop("chapters")
            course = Course(**course_data)
            db.add(course)
            db.flush()  # 获取课程ID

            for chapter_data in chapters:
                logger.info(f"创建章节: {chapter_data['title']}")
                chapter_data["course_id"] = course.id
                chapter = Chapter(**chapter_data)
                db.add(chapter)

        db.commit()
        logger.info("课程数据创建成功")
        
    except Exception as e:
        logger.error(f"初始化课程数据失败: {str(e)}")
        db.rollback()
        raise

if __name__ == "__main__":
    try:
        db = next(get_db())
        init_courses(db)
        print("课程初始化成功")
    except Exception as e:
        print(f"课程初始化失败: {str(e)}") 