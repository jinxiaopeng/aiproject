from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..services import alert_rules
from ..schemas.alert_rules import (
    AlertRuleCreate,
    AlertRuleUpdate,
    AlertRuleResponse,
    AlertRuleList
)
from ..core.auth import get_current_user

router = APIRouter()

@router.post("", response_model=AlertRuleResponse)
async def create_rule(
    rule: AlertRuleCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """创建预警规则"""
    return alert_rules.create_alert_rule(db, current_user["id"], rule)

@router.get("", response_model=AlertRuleList)
async def get_rules(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    metric_type: Optional[str] = None,
    enabled: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取预警规则列表"""
    rules, total = alert_rules.get_alert_rules(
        db,
        current_user["id"],
        skip=skip,
        limit=limit,
        metric_type=metric_type,
        enabled=enabled
    )
    return AlertRuleList(total=total, items=rules)

@router.get("/{rule_id}", response_model=AlertRuleResponse)
async def get_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取单个预警规则"""
    rule = alert_rules.get_alert_rule(db, rule_id)
    if not rule or rule.user_id != current_user["id"]:
        raise HTTPException(status_code=404, detail="预警规则不存在")
    return rule

@router.put("/{rule_id}", response_model=AlertRuleResponse)
async def update_rule(
    rule_id: int,
    rule_update: AlertRuleUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """更新预警规则"""
    updated_rule = alert_rules.update_alert_rule(
        db,
        rule_id,
        current_user["id"],
        rule_update
    )
    if not updated_rule:
        raise HTTPException(status_code=404, detail="预警规则不存在")
    return updated_rule

@router.delete("/{rule_id}")
async def delete_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """删除预警规则"""
    success = alert_rules.delete_alert_rule(db, rule_id, current_user["id"])
    if not success:
        raise HTTPException(status_code=404, detail="预警规则不存在")
    return {"message": "预警规则已删除"} 