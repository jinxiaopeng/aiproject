import os
import sys
from pathlib import Path
import subprocess
import argparse
import mysql.connector
from dotenv import load_dotenv

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# 加载环境变量
load_dotenv(project_root / "backend" / ".env")

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("错误: 需要Python 3.8或更高版本")
        sys.exit(1)

def check_dependencies():
    """检查依赖项"""
    requirements_file = project_root / "backend" / "requirements.txt"
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"错误: 安装依赖项失败: {e}")
        sys.exit(1)

def check_database():
    """检查数据库连接"""
    try:
        # 尝试连接数据库
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "jxp1210"),
            database=os.getenv("DB_NAME", "wsirp_db")
        )
        conn.close()
        print("数据库连接成功")
    except mysql.connector.Error as e:
        print(f"错误: 数据库连接失败: {e}")
        sys.exit(1)

def init_database():
    """初始化数据库"""
    try:
        # 运行数据库初始化脚本
        init_script = project_root / "scripts" / "init_db.py"
        subprocess.run(
            [sys.executable, str(init_script)],
            check=True
        )
        print("数据库初始化成功")
    except subprocess.CalledProcessError as e:
        print(f"错误: 数据库初始化失败: {e}")
        sys.exit(1)

def create_directories():
    """创建必要的目录"""
    dirs = [
        "data",
        "data/uploads",
        "data/labs",
        "logs",
        "temp",
        "cache"
    ]
    
    for dir_name in dirs:
        dir_path = project_root / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"创建目录: {dir_path}")

def start_application(args):
    """启动应用"""
    try:
        env = os.environ.copy()
        
        # 设置环境变量
        if args.debug:
            env["DEBUG"] = "True"
        if args.reload:
            env["RELOAD"] = "True"
        if args.workers:
            env["WORKERS"] = str(args.workers)
        if args.port:
            env["PORT"] = str(args.port)
            
        # 启动应用
        app_file = project_root / "backend" / "app.py"
        subprocess.run(
            [sys.executable, str(app_file)],
            env=env,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"错误: 应用启动失败: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n应用已停止")
        sys.exit(0)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Web安全智能学习平台启动脚本")
    parser.add_argument("--debug", action="store_true", help="启用调试模式")
    parser.add_argument("--reload", action="store_true", help="启用自动重载")
    parser.add_argument("--workers", type=int, help="工作进程数量")
    parser.add_argument("--port", type=int, help="监听端口")
    parser.add_argument("--init-db", action="store_true", help="初始化数据库")
    args = parser.parse_args()
    
    try:
        print("正在启动Web安全智能学习平台...")
        
        # 检查环境
        check_python_version()
        print("Python版本检查通过")
        
        # 检查依赖
        check_dependencies()
        print("依赖项检查通过")
        
        # 创建目录
        create_directories()
        print("目录创建完成")
        
        # 检查数据库
        check_database()
        
        # 如果需要初始化数据库
        if args.init_db:
            init_database()
        
        # 启动应用
        start_application(args)
        
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 