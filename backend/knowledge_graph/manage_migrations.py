import os
import sys
from alembic import command
from alembic.config import Config
from pathlib import Path

# 添加项目根目录到 Python 路径
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent
sys.path.append(str(backend_dir))

def get_alembic_config():
    """获取 Alembic 配置"""
    config_file = current_dir / "alembic.ini"
    migrations_dir = current_dir / "migrations"
    
    config = Config(str(config_file))
    config.set_main_option("script_location", str(migrations_dir))
    return config

def upgrade(revision='head'):
    """升级数据库到指定版本"""
    alembic_cfg = get_alembic_config()
    command.upgrade(alembic_cfg, revision)

def downgrade(revision):
    """降级数据库到指定版本"""
    alembic_cfg = get_alembic_config()
    command.downgrade(alembic_cfg, revision)

def create_migration(message):
    """创建新的迁移版本"""
    alembic_cfg = get_alembic_config()
    command.revision(alembic_cfg, message=message, autogenerate=True)

def show_history():
    """显示迁移历史"""
    alembic_cfg = get_alembic_config()
    command.history(alembic_cfg)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Usage: python manage_migrations.py <command> [args]")
        print("Commands:")
        print("  upgrade [revision]   - 升级数据库 (默认: head)")
        print("  downgrade <revision> - 降级数据库")
        print("  create <message>     - 创建新的迁移版本")
        print("  history             - 显示迁移历史")
        sys.exit(1)

    command_name = sys.argv[1]
    try:
        if command_name == "upgrade":
            revision = sys.argv[2] if len(sys.argv) > 2 else "head"
            upgrade(revision)
            print(f"数据库已升级到版本: {revision}")
        
        elif command_name == "downgrade":
            if len(sys.argv) < 3:
                print("Error: 需要指定降级版本")
                sys.exit(1)
            downgrade(sys.argv[2])
            print(f"数据库已降级到版本: {sys.argv[2]}")
        
        elif command_name == "create":
            if len(sys.argv) < 3:
                print("Error: 需要提供迁移说明")
                sys.exit(1)
            create_migration(sys.argv[2])
            print("已创建新的迁移版本")
        
        elif command_name == "history":
            show_history()
        
        else:
            print(f"未知命令: {command_name}")
            sys.exit(1)
            
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 