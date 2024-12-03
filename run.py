import os
import sys
import subprocess
import platform
import time

def run_command(command, cwd=None):
    """运行命令并实时输出结果"""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        cwd=cwd,
        universal_newlines=True
    )
    
    while True:
        output = process.stdout.readline()
        error = process.stderr.readline()
        
        if output == '' and error == '' and process.poll() is not None:
            break
            
        if output:
            print(output.strip())
        if error:
            print(f"错误: {error.strip()}", file=sys.stderr)
            
    return process.poll()

def main():
    """主函数"""
    print("正在启动Web安全智能学习平台...")
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("错误: 需要Python 3.7或更高版本")
        sys.exit(1)
    
    # 检查操作系统
    if platform.system() != "Windows":
        print("错误: 此脚本仅支持Windows系统")
        sys.exit(1)
    
    # 创建虚拟环境
    if not os.path.exists("venv"):
        print("\n创建虚拟环境...")
        if run_command("python -m venv venv") != 0:
            print("错误: 创建虚拟环境失败")
            sys.exit(1)
    
    # 激活虚拟环境
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    venv_pip = os.path.join("venv", "Scripts", "pip.exe")
    
    # 安装依赖
    print("\n安装依赖包...")
    if run_command(f"{venv_pip} install -r requirements.txt") != 0:
        print("错误: 安装依赖包失败")
        sys.exit(1)
    
    # 初始化数据库
    print("\n初始化数据库...")
    if run_command(f"{venv_python} backend/scripts/init_db.py") != 0:
        print("错误: 初始化数据库失败")
        sys.exit(1)
    
    # 启动应用
    print("\n启动应用程序...")
    os.chdir("backend")
    run_command(f"{venv_python} -m uvicorn app:app --reload --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n正在关闭应用程序...")
        sys.exit(0)
    except Exception as e:
        print(f"\n发生错误: {str(e)}")
        sys.exit(1) 