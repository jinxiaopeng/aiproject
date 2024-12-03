from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..auth import get_current_user
from ..quiz import QuizService, get_quiz_service
from ..schemas import (
    QuizQuestionCreate,
    QuizQuestionUpdate,
    QuizQuestionResponse,
    QuizAttemptCreate,
    QuizAttemptResponse,
    User
)

router = APIRouter(prefix="/api/quiz", tags=["quiz"])

@router.get("/questions/{lesson_id}", response_model=List[QuizQuestionResponse])
async def get_quiz_questions(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    quiz_service: QuizService = Depends(get_quiz_service)
):
    """获取课时的所有测验题目"""
    return quiz_service.get_questions(lesson_id)

@router.post("/questions", response_model=QuizQuestionResponse)
async def create_quiz_question(
    question_data: QuizQuestionCreate,
    current_user: User = Depends(get_current_user),
    quiz_service: QuizService = Depends(get_quiz_service)
):
    """创建新的测验题目（仅教师和管理员）"""
    if current_user.role not in ['teacher', 'admin']:
        raise HTTPException(
            status_code=403,
            detail="没有权限创建测验题目"
        )
    return quiz_service.create_question(question_data)

@router.put("/questions/{question_id}", response_model=QuizQuestionResponse)
async def update_quiz_question(
    question_id: int,
    question_data: QuizQuestionUpdate,
    current_user: User = Depends(get_current_user),
    quiz_service: QuizService = Depends(get_quiz_service)
):
    """更新测验题目（仅教师和管理员）"""
    if current_user.role not in ['teacher', 'admin']:
        raise HTTPException(
            status_code=403,
            detail="没有权限更新测验题目"
        )
    return quiz_service.update_question(question_id, question_data)

@router.delete("/questions/{question_id}")
async def delete_quiz_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    quiz_service: QuizService = Depends(get_quiz_service)
):
    """删除测验题目（仅教师和管理员）"""
    if current_user.role not in ['teacher', 'admin']:
        raise HTTPException(
            status_code=403,
            detail="没有权限删除测验题目"
        )
    quiz_service.delete_question(question_id)
    return {"message": "题目已删除"}

@router.get("/attempts/{lesson_id}", response_model=QuizAttemptResponse)
async def get_quiz_attempt(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    quiz_service: QuizService = Depends(get_quiz_service)
):
    """获取用户的答题记录"""
    attempt = quiz_service.get_user_attempt(current_user.id, lesson_id)
    if not attempt:
        raise HTTPException(
            status_code=404,
            detail="未找到答题记录"
        )
    return attempt

@router.post("/attempts", response_model=QuizAttemptResponse)
async def submit_quiz_attempt(
    attempt_data: QuizAttemptCreate,
    current_user: User = Depends(get_current_user),
    quiz_service: QuizService = Depends(get_quiz_service)
):
    """提交答题记录"""
    return quiz_service.submit_attempt(current_user.id, attempt_data) 