import subprocess
import sys
import platform

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_wsl():
    """检查WSL状态"""
    print("\n正在检查WSL状态...")
    
    # 检查WSL功能是否启用
    success, stdout, stderr = run_command("powershell Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux")
    if success and "Enabled" in stdout:
        print("WSL功能已启用")
    else:
        print("WSL功能未启用")
        print("请以管理员身份运行以下命令启用WSL:")
        print("dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart")
        return False
    
    # 检查虚拟机平台功能
    success, stdout, stderr = run_command("powershell Get-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform")
    if success and "Enabled" in stdout:
        print("虚拟机平台功能已启用")
    else:
        print("虚拟机平台功能未启用")
        print("请以管理员身份运行以下命令启用虚拟机平台:")
        print("dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart")
        return False
    
    # 检查WSL版本
    success, stdout, stderr = run_command("wsl --list --verbose")
    if success:
        print("\nWSL发行版列表:")
        print(stdout)
        if "2" in stdout:
            print("已安装WSL2发行版")
        else:
            print("未检测到WSL2发行版，请安装一个Linux发行版并确保使用WSL2")
            print("1. 运行: wsl --set-default-version 2")
            print("2. 从Microsoft Store安装一个Linux发行版(推荐Ubuntu)")
    else:
        print("无法获取WSL发行版列表")
        print("请确保已安装WSL2内核更新包：")
        print("https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi")
        return False
    
    return True

def check_hyperv():
    """检查Hyper-V状态"""
    print("\n正在检查Hyper-V状态...")
    success, stdout, stderr = run_command("powershell Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V")
    if success and "Enabled" in stdout:
        print("Hyper-V已启用")
        return True
    else:
        print("Hyper-V未启用")
        print("请以管理员身份运行以下PowerShell命令启用Hyper-V:")
        print("Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All")
        return False

def check_docker():
    """检查Docker状态"""
    print("\n正在检查Docker状态...")
    
    # 检查Docker服务
    success, stdout, stderr = run_command("sc query docker")
    if not success or "RUNNING" not in stdout:
        print("Docker服务未运行")
        print("请启动Docker Desktop并等待其完全启动")
        return False
    
    # 检查Docker守护进程
    success, stdout, stderr = run_command("docker info")
    if success:
        print("Docker服务正常运行")
        print("Docker信息:")
        print(stdout)
        return True
    else:
        print("Docker守护进程未正常运行")
        print("错误信息:", stderr)
        print("\n请确保Docker Desktop已启动，并等待其完全启动")
        return False

def main():
    """主函数"""
    if platform.system() != "Windows":
        print("此脚本仅支持Windows系统")
        return

    print("开始检查Docker运行环境...")
    
    wsl_ok = check_wsl()
    hyperv_ok = check_hyperv()
    docker_ok = check_docker()
    
    print("\n检查结果汇总:")
    print(f"WSL状态: {'正常' if wsl_ok else '需要配置'}")
    print(f"Hyper-V状态: {'正常' if hyperv_ok else '需要配置'}")
    print(f"Docker状态: {'正常' if docker_ok else '需要配置'}")
    
    if not (wsl_ok and hyperv_ok and docker_ok):
        print("\n请按照上述提示配置环境。配置完成后需要重启电脑。")
    else:
        print("\n所有组件都已正确配置。")

if __name__ == "__main__":
    main() 