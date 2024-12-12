from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.learning import LearningService
from ..schemas.learning import (
    LearningRecordCreate,
    LearningRecordUpdate,
    LearningRecordInDB,
    StudySessionCreate,
    StudySessionUpdate,
    StudySessionInDB,
    TestRecordCreate,
    TestRecordInDB,
    LearningStats,
    LearningPath
)
from ..core.deps import get_current_user
from ..core.logger import logger

router = APIRouter(prefix="/learning", tags=["learning"])

@router.post("/records", response_model=LearningRecordInDB)
async def create_learning_record(
    record: LearningRecordCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建学习记录"""
    try:
        learning_service = LearningService(db)
        return learning_service.create_learning_record(
            user_id=current_user.id,
            entity_id=record.entity_id
        )
    except Exception as e:
        logger.error(f"创建学习记录失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建学习记录失败: {str(e)}"
        )

@router.get("/records/{entity_id}", response_model=LearningRecordInDB)
async def get_learning_record(
    entity_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取学习记录"""
    try:
        learning_service = LearningService(db)
        record = learning_service.get_learning_record(
            user_id=current_user.id,
            entity_id=entity_id
        )
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="学习记录不存在"
            )
        return record
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取学习记录失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取学习记录失败: {str(e)}"
        )

@router.put("/records/{entity_id}", response_model=LearningRecordInDB)
async def update_learning_record(
    entity_id: int,
    record_update: LearningRecordUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """更新学习记录"""
    try:
        learning_service = LearningService(db)
        return learning_service.update_learning_progress(
            user_id=current_user.id,
            entity_id=entity_id,
            progress=record_update.progress or 0.0,
            notes=record_update.notes
        )
    except Exception as e:
        logger.error(f"更新学习记录失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新学习记录失败: {str(e)}"
        )

@router.post("/sessions/start", response_model=StudySessionInDB)
async def start_study_session(
    session: StudySessionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """开始学习会话"""
    try:
        learning_service = LearningService(db)
        return learning_service.start_study_session(
            user_id=current_user.id,
            entity_id=session.learning_record_id,  # 这里使用entity_id
            notes=session.notes
        )
    except Exception as e:
        logger.error(f"开始学习会话失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"开始学习会话失败: {str(e)}"
        )

@router.put("/sessions/{session_id}/end", response_model=StudySessionInDB)
async def end_study_session(
    session_id: int,
    session_update: StudySessionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """结束学习会话"""
    try:
        learning_service = LearningService(db)
        return learning_service.end_study_session(
            session_id=session_id,
            progress_delta=session_update.progress_delta,
            notes=session_update.notes
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"结束学习会话失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"结束学习会话失败: {str(e)}"
        )

@router.post("/tests", response_model=TestRecordInDB)
async def submit_test_result(
    test: TestRecordCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """提交测试结果"""
    try:
        learning_service = LearningService(db)
        return learning_service.submit_test_result(
            user_id=current_user.id,
            entity_id=test.learning_record_id,  # 这里使用entity_id
            score=test.score,
            max_score=test.max_score,
            answers=test.answers
        )
    except Exception as e:
        logger.error(f"提交测试结果失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"提交测试结果失败: {str(e)}"
        )

@router.get("/stats", response_model=LearningStats)
async def get_learning_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取学习统计信息"""
    try:
        learning_service = LearningService(db)
        return learning_service.get_learning_stats(current_user.id)
    except Exception as e:
        logger.error(f"获取学习统计失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取学习统计失败: {str(e)}"
        )

@router.get("/path/{entity_id}", response_model=LearningPath)
async def get_learning_path(
    entity_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取学习路径"""
    try:
        learning_service = LearningService(db)
        return learning_service.get_learning_path(
            user_id=current_user.id,
            entity_id=entity_id
        )
    except Exception as e:
        logger.error(f"获取学习路径失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取学习路径失败: {str(e)}"
        )
``` 