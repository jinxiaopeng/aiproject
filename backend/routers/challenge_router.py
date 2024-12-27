"""
靶场系统路由
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Dict, List
import subprocess
import os
import shutil
from ..core.logger import get_logger
from datetime import datetime

logger = get_logger(__name__)
router = APIRouter(
    prefix="/challenges",
    tags=["challenges"]
)

# 配置上传文件保存路径
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(current_dir, "uploads", "challenges")

# 确保上传目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)
logger.info(f"Upload directory: {UPLOAD_DIR}")

@router.post("/{challenge_id}/start")
async def start_challenge(challenge_id: int) -> Dict:
    """启动靶场"""
    try:
        # 获取项目根目录
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        challenge_dir = os.path.join(current_dir, "challenges", "web_security", "sql_injection")
        
        # 切换到challenge目录
        logger.info(f"Changing directory to: {challenge_dir}")
        os.chdir(challenge_dir)
        
        # 使用docker compose启动
        result = subprocess.run(
            ["docker", "compose", "up", "-d"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            logger.error(f"启动靶场失败: {result.stderr}")
            raise Exception(f"启动失败: {result.stderr}")
            
        return {
            "success": True,
            "message": "靶场启动成功"
        }
        
    except Exception as e:
        logger.error(f"Failed to start challenge {challenge_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{challenge_id}/stop")
async def stop_challenge(challenge_id: int) -> Dict:
    """停止��场"""
    try:
        # 获取项目根目录
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        challenge_dir = os.path.join(current_dir, "challenges", "web_security", "sql_injection")
        
        # 切换到challenge目录
        logger.info(f"Changing directory to: {challenge_dir}")
        os.chdir(challenge_dir)
        
        # 使用docker compose停止
        result = subprocess.run(
            ["docker", "compose", "down"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            logger.error(f"停止靶场失败: {result.stderr}")
            raise Exception(f"停止失败: {result.stderr}")
            
        return {
            "success": True,
            "message": "靶场停止成功"
        }
        
    except Exception as e:
        logger.error(f"Failed to stop challenge {challenge_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{challenge_id}/status")
async def get_challenge_status(challenge_id: int) -> Dict:
    """获取靶场状态"""
    try:
        # 获取项目根目录
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        challenge_dir = os.path.join(current_dir, "challenges", "web_security", "sql_injection")
        
        # 切换到challenge目录
        logger.info(f"Changing directory to: {challenge_dir}")
        os.chdir(challenge_dir)
        
        # 使用docker compose ps检查状态
        result = subprocess.run(
            ["docker", "compose", "ps", "--format", "json"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise Exception(f"获取状态失败: {result.stderr}")
            
        return {
            "success": True,
            "status": result.stdout
        }
        
    except Exception as e:
        logger.error(f"Failed to get challenge status {challenge_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_challenge_files(files: List[UploadFile] = File(...)):
    """
    上传题目相关文件
    """
    try:
        uploaded_files = []
        
        # 创建以时间戳命名的文件夹
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        challenge_dir = os.path.join(UPLOAD_DIR, timestamp)
        os.makedirs(challenge_dir, exist_ok=True)
        
        logger.info(f"Created challenge directory: {challenge_dir}")
        
        for file in files:
            # 检查文件大小（10MB限制）
            file_size = 0
            
            # 创建临时文件来保存
            temp_file_path = os.path.join(challenge_dir, file.filename)
            logger.info(f"Saving file to: {temp_file_path}")
            
            try:
                # 重置文件指针
                await file.seek(0)
                
                # 直接保存文件
                contents = await file.read()
                file_size = len(contents)
                
                if file_size > 10 * 1024 * 1024:  # 10MB
                    raise HTTPException(
                        status_code=400,
                        detail=f"文件 {file.filename} 超过10MB限制"
                    )
                
                with open(temp_file_path, "wb") as f:
                    f.write(contents)
                
                logger.info(f"Successfully saved file: {file.filename}, size: {file_size}")
                
                # 记录上传的文件信息
                uploaded_files.append({
                    "filename": file.filename,
                    "size": file_size,
                    "path": temp_file_path
                })
                
            except Exception as e:
                logger.error(f"Error saving file {file.filename}: {str(e)}")
                raise
        
        return {
            "message": "文件上传成功",
            "challenge_id": timestamp,
            "files": uploaded_files
        }
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        # 如果出错，清理已上传的文件
        if os.path.exists(challenge_dir):
            shutil.rmtree(challenge_dir)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/files/{challenge_id}")
async def get_challenge_files(challenge_id: str):
    """
    获取题目的文件列表
    """
    challenge_dir = os.path.join(UPLOAD_DIR, challenge_id)
    if not os.path.exists(challenge_dir):
        raise HTTPException(status_code=404, detail="题目文件不存在")
    
    files = []
    for filename in os.listdir(challenge_dir):
        file_path = os.path.join(challenge_dir, filename)
        files.append({
            "filename": filename,
            "size": os.path.getsize(file_path),
            "path": file_path
        })
    
    return files 