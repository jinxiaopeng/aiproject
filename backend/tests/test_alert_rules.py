import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from monitor_service.models.alert_rules import AlertRule, MetricType, ComparisonOperator
from monitor_service.services.alert_rules import (
    create_alert_rule,
    get_alert_rule,
    get_alert_rules,
    update_alert_rule,
    delete_alert_rule,
    update_rule_last_triggered,
    get_active_rules_by_metric
)
from monitor_service.schemas.alert_rules import AlertRuleCreate, AlertRuleUpdate

@pytest.fixture
def sample_rule():
    return {
        "name": "Test CPU Alert",
        "description": "Test CPU usage alert rule",
        "metric_type": MetricType.CPU,
        "operator": ComparisonOperator.GT,
        "threshold": 80.0,
        "duration": 0,
        "enabled": True,
        "notify_methods": ["web"],
        "cooldown": 300
    }

def test_create_alert_rule(db: Session, sample_rule):
    """测试创建预警规则"""
    rule_create = AlertRuleCreate(**sample_rule)
    user_id = 1
    
    rule = create_alert_rule(db, user_id, rule_create)
    
    assert rule.id is not None
    assert rule.user_id == user_id
    assert rule.name == sample_rule["name"]
    assert rule.metric_type == sample_rule["metric_type"]
    assert rule.threshold == sample_rule["threshold"]
    assert rule.enabled == sample_rule["enabled"]

def test_get_alert_rule(db: Session, sample_rule):
    """测试获取单个预警规则"""
    # 创建规则
    rule_create = AlertRuleCreate(**sample_rule)
    user_id = 1
    created_rule = create_alert_rule(db, user_id, rule_create)
    
    # 获取规则
    rule = get_alert_rule(db, created_rule.id)
    
    assert rule is not None
    assert rule.id == created_rule.id
    assert rule.name == sample_rule["name"]

def test_get_alert_rules(db: Session, sample_rule):
    """测试获取预警规则列表"""
    user_id = 1
    
    # 创建多个规则
    rule_create = AlertRuleCreate(**sample_rule)
    create_alert_rule(db, user_id, rule_create)
    
    sample_rule["name"] = "Test Memory Alert"
    sample_rule["metric_type"] = MetricType.MEMORY
    rule_create = AlertRuleCreate(**sample_rule)
    create_alert_rule(db, user_id, rule_create)
    
    # 获取规则列表
    rules, total = get_alert_rules(db, user_id)
    
    assert total == 2
    assert len(rules) == 2
    assert rules[0].metric_type == MetricType.MEMORY
    assert rules[1].metric_type == MetricType.CPU

def test_update_alert_rule(db: Session, sample_rule):
    """测试更新预警规则"""
    # 创建规则
    rule_create = AlertRuleCreate(**sample_rule)
    user_id = 1
    created_rule = create_alert_rule(db, user_id, rule_create)
    
    # 更新规则
    update_data = AlertRuleUpdate(
        name="Updated CPU Alert",
        threshold=90.0,
        enabled=False
    )
    
    updated_rule = update_alert_rule(db, created_rule.id, user_id, update_data)
    
    assert updated_rule is not None
    assert updated_rule.name == "Updated CPU Alert"
    assert updated_rule.threshold == 90.0
    assert not updated_rule.enabled

def test_delete_alert_rule(db: Session, sample_rule):
    """测试删除预警规则"""
    # 创建规则
    rule_create = AlertRuleCreate(**sample_rule)
    user_id = 1
    created_rule = create_alert_rule(db, user_id, rule_create)
    
    # 删除规则
    success = delete_alert_rule(db, created_rule.id, user_id)
    
    assert success
    assert get_alert_rule(db, created_rule.id) is None

def test_update_rule_last_triggered(db: Session, sample_rule):
    """测试更新规则的最后触发时间"""
    # 创建规则
    rule_create = AlertRuleCreate(**sample_rule)
    user_id = 1
    created_rule = create_alert_rule(db, user_id, rule_create)
    
    # 更新最后触发时间
    before_update = datetime.utcnow() - timedelta(seconds=1)
    update_rule_last_triggered(db, created_rule.id)
    
    # 获取更新后的规则
    updated_rule = get_alert_rule(db, created_rule.id)
    
    assert updated_rule.last_triggered is not None
    assert updated_rule.last_triggered > before_update

def test_get_active_rules_by_metric(db: Session, sample_rule):
    """测试获取指定指标类型的活动规则"""
    user_id = 1
    
    # 创建启用的规则
    rule_create = AlertRuleCreate(**sample_rule)
    create_alert_rule(db, user_id, rule_create)
    
    # 创建禁用的规则
    sample_rule["enabled"] = False
    rule_create = AlertRuleCreate(**sample_rule)
    create_alert_rule(db, user_id, rule_create)
    
    # 获取活动规则
    active_rules = get_active_rules_by_metric(db, MetricType.CPU)
    
    assert len(active_rules) == 1
    assert active_rules[0].enabled
    assert active_rules[0].metric_type == MetricType.CPU

def test_filter_alert_rules(db: Session, sample_rule):
    """测试预警规则过滤"""
    user_id = 1
    
    # 创建CPU规则
    rule_create = AlertRuleCreate(**sample_rule)
    create_alert_rule(db, user_id, rule_create)
    
    # 创建内存规则
    sample_rule["name"] = "Test Memory Alert"
    sample_rule["metric_type"] = MetricType.MEMORY
    rule_create = AlertRuleCreate(**sample_rule)
    create_alert_rule(db, user_id, rule_create)
    
    # 测试按指标类型过滤
    rules, total = get_alert_rules(db, user_id, metric_type=MetricType.CPU)
    assert total == 1
    assert rules[0].metric_type == MetricType.CPU
    
    # 测试按启用状态过滤
    rules, total = get_alert_rules(db, user_id, enabled=True)
    assert total == 2
    assert all(rule.enabled for rule in rules) 