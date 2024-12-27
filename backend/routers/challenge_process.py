"""
靶场进程管理路由
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Dict, Optional, List

from ..dependencies import get_db, get_current_user
from ..models.user import User
from ..models.challenge import Challenge
from ..core.process_manager import ProcessManager

router = APIRouter(
    prefix="/api/challenges",
    tags=["challenge_process"]
)

process_manager = ProcessManager()

@router.post("/{challenge_id}/start")
async def start_process(
    challenge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict:
    """启动靶场进程"""
    challenge = db.query(Challenge).get(challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
        
    try:
        return await process_manager.start_process(challenge)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{challenge_id}/stop")
async def stop_process(
    challenge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict:
    """停止靶场进程"""
    challenge = db.query(Challenge).get(challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
        
    try:
        return await process_manager.stop_process(challenge_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{challenge_id}/restart")
async def restart_process(
    challenge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict:
    """重启靶场进程"""
    challenge = db.query(Challenge).get(challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
        
    try:
        return await process_manager.restart_process(challenge)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{challenge_id}/status")
async def get_process_status(
    challenge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Optional[Dict]:
    """获取进程状态"""
    challenge = db.query(Challenge).get(challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
        
    return process_manager.get_process_status(challenge_id)

@router.get("/running")
async def get_running_processes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[int, Dict]:
    """获取所有运行中的进程"""
    running_processes = {}
    for challenge_id in process_manager.processes.keys():
        status = process_manager.get_process_status(challenge_id)
        if status and status["status"] == "running":
            running_processes[challenge_id] = status
    return running_processes

@router.get("/{challenge_id}/logs")
async def get_process_logs(
    challenge_id: int,
    lines: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[str]:
    """获取进程日志"""
    challenge = db.query(Challenge).get(challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
        
    return process_manager.get_process_logs(challenge_id, lines)

@router.get("/{challenge_id}/logs/download")
async def download_log_file(
    challenge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> FileResponse:
    """下载日志文件"""
    challenge = db.query(Challenge).get(challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
        
    log_file = process_manager.get_log_file(challenge_id)
    if not log_file:
        raise HTTPException(status_code=404, detail="Log file not found")
        
    return FileResponse(
        log_file,
        filename=f"challenge_{challenge_id}.log",
        media_type="text/plain"
    )