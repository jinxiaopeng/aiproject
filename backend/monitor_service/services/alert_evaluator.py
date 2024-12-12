from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from ..models.alert_rules import AlertRule, MetricType
from ..models.monitor import MonitorAlert, AlertLevel, AlertStatus
from . import alert_rules
from ..core.notification import send_notification

class AlertEvaluator:
    def __init__(self, db: Session):
        self.db = db
        self.metric_cache: Dict[str, List[Dict[str, Any]]] = {}
        
    def evaluate_metric(self, metric_type: str, value: float, user_id: int, context: Dict[str, Any] = None):
        """评估单个指标是否触发预警"""
        # 获取该指标类型的所有活动规则
        rules = alert_rules.get_user_rules_by_metric(self.db, user_id, metric_type)
        
        for rule in rules:
            if not rule.enabled:
                continue
                
            # 检查冷却时间
            if rule.last_triggered:
                cooldown_end = rule.last_triggered + timedelta(seconds=rule.cooldown)
                if datetime.utcnow() < cooldown_end:
                    continue
            
            # 评估规则
            if self._evaluate_rule(rule, value):
                self._trigger_alert(rule, value, context)
    
    def _evaluate_rule(self, rule: AlertRule, value: float) -> bool:
        """评估单个规则"""
        if rule.operator == ">":
            return value > rule.threshold
        elif rule.operator == ">=":
            return value >= rule.threshold
        elif rule.operator == "<":
            return value < rule.threshold
        elif rule.operator == "<=":
            return value <= rule.threshold
        elif rule.operator == "==":
            return value == rule.threshold
        elif rule.operator == "!=":
            return value != rule.threshold
        return False
    
    def _trigger_alert(self, rule: AlertRule, value: float, context: Dict[str, Any] = None):
        """触发预警"""
        # 更新规则的最后触发时间
        alert_rules.update_rule_last_triggered(self.db, rule.id)
        
        # 创建预警记录
        alert = MonitorAlert(
            user_id=rule.user_id,
            rule_id=rule.id,
            level=self._determine_alert_level(rule.metric_type, value),
            title=f"{rule.name} 触发预警",
            content=self._generate_alert_content(rule, value, context),
            status=AlertStatus.NEW
        )
        
        self.db.add(alert)
        self.db.commit()
        
        # 发送通知
        for method in rule.notify_methods:
            try:
                send_notification(method, alert)
            except Exception as e:
                print(f"Failed to send notification via {method}: {str(e)}")
    
    def _determine_alert_level(self, metric_type: MetricType, value: float) -> AlertLevel:
        """确定预警级别"""
        if metric_type == MetricType.CPU:
            if value >= 90:
                return AlertLevel.CRITICAL
            elif value >= 80:
                return AlertLevel.ERROR
            elif value >= 70:
                return AlertLevel.WARNING
            return AlertLevel.INFO
        elif metric_type == MetricType.MEMORY:
            if value >= 95:
                return AlertLevel.CRITICAL
            elif value >= 85:
                return AlertLevel.ERROR
            elif value >= 75:
                return AlertLevel.WARNING
            return AlertLevel.INFO
        elif metric_type == MetricType.DISK:
            if value >= 95:
                return AlertLevel.CRITICAL
            elif value >= 90:
                return AlertLevel.ERROR
            elif value >= 80:
                return AlertLevel.WARNING
            return AlertLevel.INFO
        return AlertLevel.INFO
    
    def _generate_alert_content(self, rule: AlertRule, value: float, context: Dict[str, Any] = None) -> str:
        """生成预警内容"""
        content = f"监控指标 {rule.metric_type} 当前值为 {value}，"
        content += f"触发条件：{rule.metric_type} {rule.operator} {rule.threshold}"
        
        if context:
            content += "\n\n附加信息："
            for key, val in context.items():
                content += f"\n{key}: {val}"
        
        return content