import os
import sys
import logging
from datetime import datetime, timedelta
from sqlalchemy import desc, func

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

from backend.monitor_service.database import SessionLocal
from backend.monitor_service.models.threat import ThreatEvent

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def query_recent_threats(hours=1):
    """查询最近的威胁事件"""
    try:
        db = SessionLocal()
        # 计算时间范围
        time_threshold = datetime.now() - timedelta(hours=hours)
        
        # 查询最近的威胁事件
        threats = db.query(ThreatEvent)\
            .filter(ThreatEvent.timestamp >= time_threshold)\
            .order_by(desc(ThreatEvent.timestamp))\
            .all()
        
        if not threats:
            print(f"最近{hours}小时内没有检测到威胁事件")
            return
        
        print(f"\n最近{hours}小时内检测到的威胁事件：")
        print("-" * 80)
        
        for threat in threats:
            print(f"时间: {threat.timestamp}")
            print(f"级别: {threat.level}")
            print(f"类型: {threat.type}")
            print(f"描述: {threat.description}")
            print(f"来源IP: {threat.source_ip}")
            print(f"状态: {threat.status}")
            print(f"详情: {threat.details}")
            print("-" * 80)
            
    except Exception as e:
        logger.error(f"查询失败: {str(e)}")
    finally:
        db.close()

def query_by_level(level):
    """按威胁级别查询"""
    try:
        db = SessionLocal()
        threats = db.query(ThreatEvent)\
            .filter(ThreatEvent.level == level)\
            .order_by(desc(ThreatEvent.timestamp))\
            .all()
        
        if not threats:
            print(f"没有找到级别为 {level} 的威胁事件")
            return
        
        print(f"\n级别为 {level} 的威胁事件：")
        print("-" * 80)
        
        for threat in threats:
            print(f"时间: {threat.timestamp}")
            print(f"类型: {threat.type}")
            print(f"描述: {threat.description}")
            print(f"来源IP: {threat.source_ip}")
            print(f"状态: {threat.status}")
            print("-" * 80)
            
    except Exception as e:
        logger.error(f"查询失败: {str(e)}")
    finally:
        db.close()

def show_statistics():
    """显示威胁事件统计信息"""
    try:
        db = SessionLocal()
        total = db.query(ThreatEvent).count()
        
        # 按级别统计
        level_stats = db.query(
            ThreatEvent.level,
            func.count(ThreatEvent.id).label('count')
        ).group_by(ThreatEvent.level).all()
        
        # 按类型统计
        type_stats = db.query(
            ThreatEvent.type,
            func.count(ThreatEvent.id).label('count')
        ).group_by(ThreatEvent.type).all()
        
        print("\n威胁事件统计信息：")
        print("-" * 80)
        print(f"总事件数: {total}")
        
        print("\n按级别统计：")
        for level, count in level_stats:
            print(f"{level}: {count}件")
        
        print("\n按类型统计：")
        for type_, count in type_stats:
            print(f"{type_}: {count}件")
        
    except Exception as e:
        logger.error(f"统计失败: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    print("威胁事件查询工具")
    print("1. 查看最近1小时的威胁事件")
    print("2. 查看最近24小时的威胁事件")
    print("3. 查看高危威胁事件")
    print("4. 查看统计信息")
    
    choice = input("\n请选择操作 (1-4): ")
    
    if choice == "1":
        query_recent_threats(1)
    elif choice == "2":
        query_recent_threats(24)
    elif choice == "3":
        query_by_level("HIGH")
    elif choice == "4":
        show_statistics()
    else:
        print("无效的选择") 