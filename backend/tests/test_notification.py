import pytest
from unittest.mock import patch, MagicMock
from monitor_service.core.notification import NotificationService, send_notification
from monitor_service.models.monitor import MonitorAlert, AlertLevel, AlertStatus

@pytest.fixture
def notification_service():
    return NotificationService()

@pytest.fixture
def sample_alert():
    return MonitorAlert(
        id=1,
        user_id=1,
        rule_id=1,
        level=AlertLevel.ERROR,
        title="Test Alert",
        content="Test alert content",
        status=AlertStatus.NEW
    )

def test_send_email(notification_service, sample_alert):
    """测试发送邮件通知"""
    with patch('smtplib.SMTP') as mock_smtp:
        # 设置mock SMTP服务器
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # 发送邮件
        notification_service.send_email(
            "test@example.com",
            f"[{sample_alert.level}] {sample_alert.title}",
            sample_alert.content
        )
        
        # 验证SMTP调用
        mock_smtp.assert_called_once()
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()
        mock_server.send_message.assert_called_once()

def test_send_web_notification(notification_service, sample_alert):
    """测试发送Web通知"""
    # 由于Web通知目前是空实现，我们只验证方法可以被调用
    notification_service.send_web_notification(
        sample_alert.user_id,
        sample_alert.title,
        sample_alert.content
    )

def test_send_sms(notification_service, sample_alert):
    """测试发送短信通知"""
    # 由于短信通知目前是空实现，我们只验证方法可以被调用
    notification_service.send_sms(
        "1234567890",
        f"{sample_alert.title}\n{sample_alert.content}"
    )

def test_send_notification_email(sample_alert):
    """测试通过邮件发送通知"""
    with patch('monitor_service.core.notification.notification_service.send_email') as mock_send_email:
        send_notification("email", sample_alert)
        mock_send_email.assert_called_once()

def test_send_notification_web(sample_alert):
    """测试通过Web发送通知"""
    with patch('monitor_service.core.notification.notification_service.send_web_notification') as mock_send_web:
        send_notification("web", sample_alert)
        mock_send_web.assert_called_once_with(
            sample_alert.user_id,
            f"[{sample_alert.level}] {sample_alert.title}",
            sample_alert.content
        )

def test_send_notification_sms(sample_alert):
    """测试通过短信发送通知"""
    with patch('monitor_service.core.notification.notification_service.send_sms') as mock_send_sms:
        send_notification("sms", sample_alert)
        mock_send_sms.assert_called_once()

def test_send_notification_invalid_method(sample_alert):
    """测试无效的通知方式"""
    with patch('monitor_service.core.notification.notification_service.send_email') as mock_send_email:
        send_notification("invalid", sample_alert)
        mock_send_email.assert_not_called()

def test_send_notification_with_extra_context(sample_alert):
    """测试带有额外上下文的通知"""
    extra_context = {
        "server": "prod-01",
        "timestamp": "2023-12-11 10:00:00"
    }
    
    with patch('monitor_service.core.notification.notification_service.send_email') as mock_send_email:
        send_notification("email", sample_alert, extra_context)
        
        # 验证额外上下文被添加到通知内容中
        mock_send_email.assert_called_once()
        _, _, content = mock_send_email.call_args[0]
        
        assert "server: prod-01" in content
        assert "timestamp: 2023-12-11 10:00:00" in content

def test_send_notification_handles_errors(sample_alert):
    """测试通知发送错误处理"""
    with patch('monitor_service.core.notification.notification_service.send_email') as mock_send_email:
        # 模拟发送失败
        mock_send_email.side_effect = Exception("Failed to send email")
        
        # 验证异常被捕获且不会传播
        try:
            send_notification("email", sample_alert)
        except Exception:
            pytest.fail("Exception should be caught") 