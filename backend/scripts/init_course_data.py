from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
from dotenv import load_dotenv

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.course import Course, Chapter, CourseEnrollment, ChapterProgress, CourseNote, CourseComment
from models.user import User

# 加载环境变量
load_dotenv()

# 数据库连接
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:jxp1210@localhost/app")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def create_test_data():
    # 检查是否已存在测试用户
    instructor = session.query(User).filter(User.email == "teacher@example.com").first()
    if not instructor:
        instructor = User(
            username="teacher",
            email="teacher@example.com",
            password="password123",
            role="instructor"
        )
        session.add(instructor)
        session.commit()

    student = session.query(User).filter(User.email == "student@example.com").first()
    if not student:
        student = User(
            username="student",
            email="student@example.com",
            password="password123",
            role="user"
        )
        session.add(student)
        session.commit()

    # 检查是否已存在课程
    existing_courses = session.query(Course).all()
    if existing_courses:
        print("课程数据已存在，跳过创建")
        return

    # 创建测试课程
    courses_data = [
        {
            "title": "Web安全基础入门",
            "description": "本课程将带你了解Web安全的基础知识，包括常见的漏洞类型、攻击方式和防御措施。",
            "cover_url": "https://example.com/images/web-security-basic.jpg",
            "category": "web-basic",
            "difficulty": "beginner",
            "instructor_id": instructor.id,
            "chapters": [
                {
                    "title": "Web安全概述",
                    "description": "介绍Web安全的基本概念、重要性及发展历史。",
                    "video_url": "https://example.com/videos/chapter1.mp4",
                    "duration": 45,
                    "order": 1
                },
                {
                    "title": "HTTP协议基础",
                    "description": "深入理解HTTP协议的工作原理及安全隐患。",
                    "video_url": "https://example.com/videos/chapter2.mp4",
                    "duration": 60,
                    "order": 2
                }
            ]
        },
        {
            "title": "渗透测试实战",
            "description": "通过实际案例学习渗透测试的方法和技巧，提升实战能力。",
            "cover_url": "https://example.com/images/pentest.jpg",
            "category": "pentest",
            "difficulty": "intermediate",
            "instructor_id": instructor.id,
            "chapters": [
                {
                    "title": "信息收集技术",
                    "description": "学习目标系统信息收集的各种方法和工具。",
                    "video_url": "https://example.com/videos/pentest1.mp4",
                    "duration": 90,
                    "order": 1
                },
                {
                    "title": "漏洞扫描与利用",
                    "description": "掌握常用漏洞扫描工具的使用方法。",
                    "video_url": "https://example.com/videos/pentest2.mp4",
                    "duration": 120,
                    "order": 2
                }
            ]
        }
    ]

    for course_data in courses_data:
        chapters_data = course_data.pop("chapters")
        course = Course(**course_data)
        session.add(course)
        session.commit()

        for chapter_data in chapters_data:
            chapter_data["course_id"] = course.id
            chapter = Chapter(**chapter_data)
            session.add(chapter)
        session.commit()

        # 创建课程报名记录
        enrollment = CourseEnrollment(
            user_id=student.id,
            course_id=course.id,
            progress=30.0
        )
        session.add(enrollment)
        session.commit()

        # 为第一个章节添加进度
        first_chapter = course.chapters[0]
        progress = ChapterProgress(
            user_id=student.id,
            chapter_id=first_chapter.id,
            progress=100.0,
            completed=True
        )
        session.add(progress)
        session.commit()

        # 添加课程笔记
        note = CourseNote(
            user_id=student.id,
            course_id=course.id,
            chapter_id=first_chapter.id,
            content="这是一个测试笔记，记录了学习过程中的重要知识点。"
        )
        session.add(note)
        session.commit()

        # 添加课程评论
        comment = CourseComment(
            user_id=student.id,
            course_id=course.id,
            content="课程内容很实用，讲解也很清晰。",
            rating=4.5
        )
        session.add(comment)
        session.commit()

    print("课程数据创建成功！")

if __name__ == "__main__":
    try:
        create_test_data()
        print("测试数据创建成功！")
    except Exception as e:
        print(f"创建测试数据��出错：{str(e)}")
        session.rollback()
    finally:
        session.close() 