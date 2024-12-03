from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .database import get_db
from .models import QuizQuestion, QuizAttempt, QuizAttemptDetail
from .schemas import (
    QuizQuestionCreate,
    QuizQuestionUpdate,
    QuizQuestionResponse,
    QuizAttemptCreate,
    QuizAttemptResponse
)

class QuizService:
    def __init__(self, db: Session):
        self.db = db

    def get_questions(self, lesson_id: int) -> List[QuizQuestion]:
        """获取课时的所有测验题目"""
        return self.db.query(QuizQuestion).filter(
            QuizQuestion.lesson_id == lesson_id
        ).order_by(QuizQuestion.order_num).all()

    def get_question(self, question_id: int) -> Optional[QuizQuestion]:
        """获取单个测验题目"""
        return self.db.query(QuizQuestion).filter(
            QuizQuestion.id == question_id
        ).first()

    def create_question(self, question_data: QuizQuestionCreate) -> QuizQuestion:
        """创建新的测验题目"""
        # 获取当前最大序号
        max_order = self.db.query(QuizQuestion).filter(
            QuizQuestion.lesson_id == question_data.lesson_id
        ).count()

        question = QuizQuestion(
            lesson_id=question_data.lesson_id,
            title=question_data.title,
            type=question_data.type,
            options=question_data.options,
            correct_answer=question_data.correct_answer,
            explanation=question_data.explanation,
            score=question_data.score,
            order_num=max_order + 1
        )
        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)
        return question

    def update_question(self, question_id: int, question_data: QuizQuestionUpdate) -> QuizQuestion:
        """更新测验题目"""
        question = self.get_question(question_id)
        if not question:
            raise HTTPException(
                status_code=404,
                detail="题目不存在"
            )

        for key, value in question_data.dict(exclude_unset=True).items():
            setattr(question, key, value)

        self.db.commit()
        self.db.refresh(question)
        return question

    def delete_question(self, question_id: int) -> None:
        """删除测验题目"""
        question = self.get_question(question_id)
        if not question:
            raise HTTPException(
                status_code=404,
                detail="题目不存在"
            )

        self.db.delete(question)
        self.db.commit()

    def get_user_attempt(self, user_id: int, lesson_id: int) -> Optional[QuizAttempt]:
        """获取用户的答题记录"""
        return self.db.query(QuizAttempt).filter(
            QuizAttempt.user_id == user_id,
            QuizAttempt.lesson_id == lesson_id
        ).first()

    def submit_attempt(self, user_id: int, attempt_data: QuizAttemptCreate) -> QuizAttempt:
        """提交答题记录"""
        # 检查是否已经提交过
        existing_attempt = self.get_user_attempt(user_id, attempt_data.lesson_id)
        if existing_attempt:
            raise HTTPException(
                status_code=400,
                detail="已经提交过答案"
            )

        # 获取所有题目
        questions = self.get_questions(attempt_data.lesson_id)
        if not questions:
            raise HTTPException(
                status_code=404,
                detail="未找到测验题目"
            )

        # 计算得分
        total_score = 0
        details = []
        for question in questions:
            user_answer = attempt_data.answers.get(str(question.id))
            if user_answer is None:
                continue

            is_correct = self._check_answer(question, user_answer)
            score = question.score if is_correct else 0
            total_score += score

            details.append(QuizAttemptDetail(
                question_id=question.id,
                user_answer=user_answer,
                is_correct=is_correct,
                score=score
            ))

        # 计算是否通过（60分及格）
        total_possible_score = sum(q.score for q in questions)
        passed = (total_score / total_possible_score) >= 0.6 if total_possible_score > 0 else False

        # 创建答题记录
        attempt = QuizAttempt(
            user_id=user_id,
            lesson_id=attempt_data.lesson_id,
            answers=attempt_data.answers,
            score=total_score,
            passed=passed
        )
        self.db.add(attempt)
        self.db.commit()

        # 添加答题详情
        for detail in details:
            detail.attempt_id = attempt.id
            self.db.add(detail)

        self.db.commit()
        self.db.refresh(attempt)
        return attempt

    def _check_answer(self, question: QuizQuestion, user_answer: Any) -> bool:
        """检查答案是否正确"""
        if question.type == 'single_choice':
            return user_answer == question.correct_answer
        elif question.type == 'multiple_choice':
            return set(user_answer) == set(question.correct_answer)
        elif question.type == 'true_false':
            return user_answer == question.correct_answer
        return False

def get_quiz_service(db: Session = Depends(get_db)) -> QuizService:
    return QuizService(db) 