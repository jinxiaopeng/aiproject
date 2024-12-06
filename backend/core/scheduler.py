from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from sqlalchemy.orm import Session
from core.database import SessionLocal
from core.docker import docker_manager
from models import ChallengeInstance

scheduler = AsyncIOScheduler()

async def cleanup_expired_instances():
    """清理过期的Docker容器"""
    db = SessionLocal()
    try:
        # 获取所有过期的实例
        expired_instances = db.query(ChallengeInstance).filter(
            ChallengeInstance.expires_at <= datetime.utcnow(),
            ChallengeInstance.is_active == True
        ).all()
        
        for instance in expired_instances:
            try:
                # 停止并删除容器
                await docker_manager.stop_container(instance.container_id)
                # 更新实例状态
                instance.is_active = False
                db.commit()
            except Exception as e:
                print(f"Failed to cleanup instance {instance.id}: {str(e)}")
                db.rollback()
    finally:
        db.close()

def start():
    """启动调度器"""
    # 每5分钟检查一次过期的容器
    scheduler.add_job(
        cleanup_expired_instances,
        trigger=IntervalTrigger(minutes=5),
        id='cleanup_expired_instances',
        replace_existing=True
    )
    scheduler.start()

def shutdown():
    """关闭调度器"""
    scheduler.shutdown()