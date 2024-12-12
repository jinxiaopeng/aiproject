from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime
from ..models.alert_rules import AlertRule
from ..schemas.alert_rules import AlertRuleCreate, AlertRuleUpdate

def create_alert_rule(db: Session, user_id: int, rule: AlertRuleCreate) -> AlertRule:
    """创建预警规则"""
    db_rule = AlertRule(
        user_id=user_id,
        **rule.model_dump()
    )
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

def get_alert_rule(db: Session, rule_id: int) -> Optional[AlertRule]:
    """获取单个预警规则"""
    return db.query(AlertRule).filter(AlertRule.id == rule_id).first()

def get_alert_rules(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    metric_type: Optional[str] = None,
    enabled: Optional[bool] = None
) -> tuple[List[AlertRule], int]:
    """获取预警规则列表"""
    query = db.query(AlertRule).filter(AlertRule.user_id == user_id)
    
    if metric_type:
        query = query.filter(AlertRule.metric_type == metric_type)
    if enabled is not None:
        query = query.filter(AlertRule.enabled == enabled)
    
    total = query.count()
    rules = query.order_by(desc(AlertRule.created_at)).offset(skip).limit(limit).all()
    
    return rules, total

def update_alert_rule(
    db: Session,
    rule_id: int,
    user_id: int,
    rule_update: AlertRuleUpdate
) -> Optional[AlertRule]:
    """更新预警规则"""
    db_rule = db.query(AlertRule).filter(
        AlertRule.id == rule_id,
        AlertRule.user_id == user_id
    ).first()
    
    if not db_rule:
        return None
    
    for key, value in rule_update.model_dump(exclude_unset=True).items():
        setattr(db_rule, key, value)
    
    db_rule.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_rule)
    return db_rule

def delete_alert_rule(db: Session, rule_id: int, user_id: int) -> bool:
    """删除预警规则"""
    result = db.query(AlertRule).filter(
        AlertRule.id == rule_id,
        AlertRule.user_id == user_id
    ).delete()
    db.commit()
    return result > 0

def update_rule_last_triggered(db: Session, rule_id: int) -> None:
    """更新规则的最后触发时间"""
    db.query(AlertRule).filter(AlertRule.id == rule_id).update({
        "last_triggered": datetime.utcnow()
    })
    db.commit()

def get_active_rules_by_metric(db: Session, metric_type: str) -> List[AlertRule]:
    """获取指定指标类型的所有启用的规则"""
    return db.query(AlertRule).filter(
        AlertRule.metric_type == metric_type,
        AlertRule.enabled == True
    ).all()

def get_user_rules_by_metric(db: Session, user_id: int, metric_type: str) -> List[AlertRule]:
    """获取用户指定指标类型的所有规则"""
    return db.query(AlertRule).filter(
        AlertRule.user_id == user_id,
        AlertRule.metric_type == metric_type
    ).all() 