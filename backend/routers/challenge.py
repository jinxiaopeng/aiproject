from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
import shutil
from datetime import datetime

router = APIRouter(prefix="/api/challenges", tags=["challenges"])

# 配置上传文件保存路径
UPLOAD_DIR = "uploads/challenges"

# 确保上传目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
        
        for file in files:
            # 检查文件大小（10MB限制）
            file_size = 0
            chunk_size = 1024 * 1024  # 1MB
            
            # 创建临时文件来检查大小
            temp_file_path = os.path.join(challenge_dir, file.filename)
            with open(temp_file_path, "wb") as buffer:
                while True:
                    chunk = await file.read(chunk_size)
                    if not chunk:
                        break
                    file_size += len(chunk)
                    if file_size > 10 * 1024 * 1024:  # 10MB
                        os.remove(temp_file_path)
                        raise HTTPException(
                            status_code=400,
                            detail=f"文件 {file.filename} 超过10MB限制"
                        )
                    buffer.write(chunk)
            
            # 记录上传的文件信息
            uploaded_files.append({
                "filename": file.filename,
                "size": file_size,
                "path": temp_file_path
            })
        
        return {
            "message": "文件上传成功",
            "challenge_id": timestamp,
            "files": uploaded_files
        }
        
    except Exception as e:
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