import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from monitor_service.models.alert_rules import AlertRule, MetricType, ComparisonOperator
from monitor_service.models.monitor import MonitorAlert, AlertLevel, AlertStatus
from monitor_service.services.alert_evaluator import AlertEvaluator
from monitor_service.services.alert_rules import create_alert_rule
from monitor_service.schemas.alert_rules import AlertRuleCreate

@pytest.fixture
def alert_evaluator(db: Session):
    return AlertEvaluator(db)

@pytest.fixture
def sample_rules(db: Session):
    rules = []
    
    # CPU规则
    cpu_rule = AlertRuleCreate(
        name="High CPU Usage",
        description="CPU usage is too high",
        metric_type=MetricType.CPU,
        operator=ComparisonOperator.GT,
        threshold=80.0,
        duration=0,
        enabled=True,
        notify_methods=["web"],
        cooldown=300
    )
    rules.append(create_alert_rule(db, 1, cpu_rule))
    
    # 内存规则
    memory_rule = AlertRuleCreate(
        name="High Memory Usage",
        description="Memory usage is too high",
        metric_type=MetricType.MEMORY,
        operator=ComparisonOperator.GT,
        threshold=90.0,
        duration=0,
        enabled=True,
        notify_methods=["web"],
        cooldown=300
    )
    rules.append(create_alert_rule(db, 1, memory_rule))
    
    # 禁用的规则
    disabled_rule = AlertRuleCreate(
        name="Disabled Rule",
        description="This rule is disabled",
        metric_type=MetricType.CPU,
        operator=ComparisonOperator.GT,
        threshold=70.0,
        duration=0,
        enabled=False,
        notify_methods=["web"],
        cooldown=300
    )
    rules.append(create_alert_rule(db, 1, disabled_rule))
    
    return rules

def test_evaluate_metric_triggers_alert(db: Session, alert_evaluator, sample_rules):
    """测试指标评估触发预警"""
    # 评估CPU指标
    alert_evaluator.evaluate_metric(MetricType.CPU, 85.0, 1)
    
    # 验证是否创建了预警记录
    alerts = db.query(MonitorAlert).all()
    assert len(alerts) == 1
    assert alerts[0].rule_id == sample_rules[0].id
    assert alerts[0].level == AlertLevel.ERROR
    assert alerts[0].status == AlertStatus.NEW

def test_evaluate_metric_respects_cooldown(db: Session, alert_evaluator, sample_rules):
    """测试预警冷却时间"""
    # 第一次触发预警
    alert_evaluator.evaluate_metric(MetricType.CPU, 85.0, 1)
    
    # 立即再次评估
    alert_evaluator.evaluate_metric(MetricType.CPU, 85.0, 1)
    
    # 验证只创建了一条预警记录
    alerts = db.query(MonitorAlert).all()
    assert len(alerts) == 1

def test_evaluate_metric_multiple_rules(db: Session, alert_evaluator, sample_rules):
    """测试多个规则的评估"""
    # 评估CPU和内存指标
    alert_evaluator.evaluate_metric(MetricType.CPU, 85.0, 1)
    alert_evaluator.evaluate_metric(MetricType.MEMORY, 95.0, 1)
    
    # 验证创建了两条预警记录
    alerts = db.query(MonitorAlert).all()
    assert len(alerts) == 2
    
    # 验证预警级别
    cpu_alert = next(a for a in alerts if a.rule_id == sample_rules[0].id)
    memory_alert = next(a for a in alerts if a.rule_id == sample_rules[1].id)
    
    assert cpu_alert.level == AlertLevel.ERROR
    assert memory_alert.level == AlertLevel.CRITICAL

def test_evaluate_metric_disabled_rule(db: Session, alert_evaluator, sample_rules):
    """测试禁用规则不触发预警"""
    # 评估CPU指标（针对禁用的规则）
    alert_evaluator.evaluate_metric(MetricType.CPU, 75.0, 1)
    
    # 验证没有创建预警记录
    alerts = db.query(MonitorAlert).filter_by(rule_id=sample_rules[2].id).all()
    assert len(alerts) == 0

def test_evaluate_metric_different_operators(db: Session, alert_evaluator):
    """测试不同比较运算符的评估"""
    user_id = 1
    
    # 创建使用不同运算符的规则
    operators = {
        ComparisonOperator.GT: (80.0, 85.0, 75.0),  # threshold, trigger_value, non_trigger_value
        ComparisonOperator.GTE: (80.0, 80.0, 79.9),
        ComparisonOperator.LT: (80.0, 75.0, 85.0),
        ComparisonOperator.LTE: (80.0, 80.0, 80.1),
        ComparisonOperator.EQ: (80.0, 80.0, 80.1),
        ComparisonOperator.NEQ: (80.0, 85.0, 80.0)
    }
    
    for operator, (threshold, trigger_value, non_trigger_value) in operators.items():
        rule = AlertRuleCreate(
            name=f"Test {operator} Rule",
            metric_type=MetricType.CPU,
            operator=operator,
            threshold=threshold,
            duration=0,
            enabled=True,
            notify_methods=["web"],
            cooldown=300
        )
        created_rule = create_alert_rule(db, user_id, rule)
        
        # 测试触发值
        alert_evaluator.evaluate_metric(MetricType.CPU, trigger_value, user_id)
        alerts = db.query(MonitorAlert).filter_by(rule_id=created_rule.id).all()
        assert len(alerts) == 1, f"Operator {operator} should trigger with value {trigger_value}"
        
        # 清除预警记录
        db.query(MonitorAlert).delete()
        db.commit()
        
        # 测试非触发值
        alert_evaluator.evaluate_metric(MetricType.CPU, non_trigger_value, user_id)
        alerts = db.query(MonitorAlert).filter_by(rule_id=created_rule.id).all()
        assert len(alerts) == 0, f"Operator {operator} should not trigger with value {non_trigger_value}"

def test_alert_level_determination(db: Session, alert_evaluator):
    """测试预警级别的确定"""
    user_id = 1
    thresholds = {
        MetricType.CPU: [
            (95.0, AlertLevel.CRITICAL),
            (85.0, AlertLevel.ERROR),
            (75.0, AlertLevel.WARNING),
            (65.0, AlertLevel.INFO)
        ],
        MetricType.MEMORY: [
            (95.0, AlertLevel.CRITICAL),
            (85.0, AlertLevel.ERROR),
            (75.0, AlertLevel.WARNING),
            (65.0, AlertLevel.INFO)
        ]
    }
    
    for metric_type, levels in thresholds.items():
        for threshold, expected_level in levels:
            rule = AlertRuleCreate(
                name=f"Test {metric_type} Level Rule",
                metric_type=metric_type,
                operator=ComparisonOperator.GT,
                threshold=threshold,
                duration=0,
                enabled=True,
                notify_methods=["web"],
                cooldown=300
            )
            created_rule = create_alert_rule(db, user_id, rule)
            
            # 评估指标
            alert_evaluator.evaluate_metric(metric_type, threshold + 1, user_id)
            
            # 验证预警级别
            alert = db.query(MonitorAlert).filter_by(rule_id=created_rule.id).first()
            assert alert.level == expected_level
            
            # 清除预警记录
            db.query(MonitorAlert).delete()
            db.commit() 