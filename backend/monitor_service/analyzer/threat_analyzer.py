import logging
from typing import Dict, List
from datetime import datetime, timedelta
import ipaddress
import re

class ThreatAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.threat_patterns = self._load_threat_patterns()
        self.known_malicious_ips = set()
        self.suspicious_patterns = {}
        self.alert_history = []
        
    def _load_threat_patterns(self) -> Dict:
        """加载威胁模式"""
        return {
            'port_scan': {
                'description': '端口扫描行为',
                'threshold': 20,  # 短时间内扫描端口数量阈值
                'time_window': 60  # 时间窗口（秒）
            },
            'brute_force': {
                'description': '暴力破解尝试',
                'threshold': 10,  # 失败尝试次数阈值
                'time_window': 300  # 时间窗口（秒）
            },
            'ddos': {
                'description': 'DDoS攻击',
                'threshold': 1000,  # 请求数量阈值
                'time_window': 60  # 时间窗口（秒）
            },
            'data_exfiltration': {
                'description': '数据外泄',
                'threshold': 10000000,  # 数据传输量阈值（字节）
                'time_window': 3600  # 时间窗口（秒）
            }
        }

    def analyze_network_data(self, network_data: Dict) -> List[Dict]:
        """分析网络数据并识别潜在威胁"""
        threats = []
        try:
            # 分析基本网络统计
            if 'basic_stats' in network_data:
                threats.extend(self._analyze_basic_stats(network_data['basic_stats']))
            
            # 分析连接
            if 'connections' in network_data:
                threats.extend(self._analyze_connections(network_data['connections']))
            
            # 分析流量模式
            if 'traffic_pattern' in network_data:
                threats.extend(self._analyze_traffic_patterns(network_data['traffic_pattern']))
            
            # 分析可疑活动
            if 'suspicious_activity' in network_data:
                threats.extend(self._analyze_suspicious_activity(network_data['suspicious_activity']))
            
            # 更新警报历史
            self._update_alert_history(threats)
            
            return threats
        except Exception as e:
            self.logger.error(f"Failed to analyze network data: {str(e)}")
            return []

    def _analyze_basic_stats(self, stats: Dict) -> List[Dict]:
        """分析基本网络统计数据"""
        threats = []
        try:
            # 检查错误率
            total_packets = stats['packets_sent'] + stats['packets_recv']
            if total_packets > 0:
                error_rate = (stats['errin'] + stats['errout']) / total_packets
                if error_rate > 0.1:  # 错误率超过10%
                    threats.append({
                        'type': 'network_error',
                        'level': 'warning',
                        'description': f'High network error rate: {error_rate:.2%}',
                        'timestamp': datetime.now().isoformat()
                    })
            
            # 检查丢包率
            if total_packets > 0:
                drop_rate = (stats['dropin'] + stats['dropout']) / total_packets
                if drop_rate > 0.05:  # 丢包率超过5%
                    threats.append({
                        'type': 'packet_loss',
                        'level': 'warning',
                        'description': f'High packet drop rate: {drop_rate:.2%}',
                        'timestamp': datetime.now().isoformat()
                    })
        except Exception as e:
            self.logger.error(f"Failed to analyze basic stats: {str(e)}")
        return threats

    def _analyze_connections(self, connections: List[Dict]) -> List[Dict]:
        """分析网络连接"""
        threats = []
        try:
            # 统计每个远程IP的连接数
            ip_connections = {}
            for conn in connections:
                if conn['remote_ip']:
                    ip = conn['remote_ip']
                    ip_connections[ip] = ip_connections.get(ip, 0) + 1
            
            # 检查连接集中度
            for ip, count in ip_connections.items():
                if count > 50:  # 单个IP建立了过多连接
                    threats.append({
                        'type': 'connection_flood',
                        'level': 'warning',
                        'description': f'High number of connections from {ip}: {count}',
                        'source_ip': ip,
                        'timestamp': datetime.now().isoformat()
                    })
                
                # 检查是否是内网IP
                try:
                    if ipaddress.ip_address(ip).is_private:
                        if count > 100:  # 内网IP建立了异常多的连接
                            threats.append({
                                'type': 'internal_scan',
                                'level': 'high',
                                'description': f'Suspicious internal network scanning from {ip}',
                                'source_ip': ip,
                                'timestamp': datetime.now().isoformat()
                            })
                except ValueError:
                    pass
        except Exception as e:
            self.logger.error(f"Failed to analyze connections: {str(e)}")
        return threats

    def _analyze_traffic_patterns(self, pattern: Dict) -> List[Dict]:
        """分析流量模式"""
        threats = []
        try:
            # 检查高频连接
            if 'high_frequency_connections' in pattern:
                for ip_port, count in pattern['high_frequency_connections'].items():
                    if count > 1000:  # 极高频率的连接
                        threats.append({
                            'type': 'high_frequency',
                            'level': 'high',
                            'description': f'Extremely high frequency connections to {ip_port}',
                            'connection': ip_port,
                            'count': count,
                            'timestamp': datetime.now().isoformat()
                        })
            
            # 检查连接总数的突然增加
            if 'total_active_connections' in pattern:
                if pattern['total_active_connections'] > 1000:
                    threats.append({
                        'type': 'connection_spike',
                        'level': 'medium',
                        'description': 'Sudden spike in total connections',
                        'count': pattern['total_active_connections'],
                        'timestamp': datetime.now().isoformat()
                    })
        except Exception as e:
            self.logger.error(f"Failed to analyze traffic patterns: {str(e)}")
        return threats

    def _analyze_suspicious_activity(self, suspicious: List[Dict]) -> List[Dict]:
        """分析可疑活动"""
        threats = []
        try:
            for activity in suspicious:
                # 根据原因确定威胁等级
                level = 'low'
                if activity['reason'] == 'Known suspicious IP':
                    level = 'high'
                elif activity['reason'] == 'Remote access port':
                    level = 'medium'
                elif activity['reason'] == 'High frequency connection':
                    level = 'medium'
                
                threats.append({
                    'type': 'suspicious_activity',
                    'level': level,
                    'description': f"Suspicious activity detected: {activity['reason']}",
                    'source_ip': activity['ip'],
                    'port': activity['port'],
                    'timestamp': datetime.now().isoformat()
                })
                
                # 更新已知恶意IP列表
                if level == 'high':
                    self.known_malicious_ips.add(activity['ip'])
        except Exception as e:
            self.logger.error(f"Failed to analyze suspicious activity: {str(e)}")
        return threats

    def _update_alert_history(self, threats: List[Dict]):
        """更新警报历史"""
        try:
            # 添加新的警报
            self.alert_history.extend(threats)
            
            # 移除超过24小时的警报
            cutoff_time = datetime.now() - timedelta(hours=24)
            self.alert_history = [
                alert for alert in self.alert_history
                if datetime.fromisoformat(alert['timestamp']) > cutoff_time
            ]
        except Exception as e:
            self.logger.error(f"Failed to update alert history: {str(e)}")

    def get_threat_summary(self) -> Dict:
        """获取威胁摘要"""
        try:
            # 按级别统计警报
            level_counts = {
                'high': 0,
                'medium': 0,
                'low': 0,
                'warning': 0
            }
            
            # 按类型统计警报
            type_counts = {}
            
            # 最近的高危警报
            recent_high_threats = []
            
            for alert in self.alert_history:
                # 统计级别
                level_counts[alert['level']] = level_counts.get(alert['level'], 0) + 1
                
                # 统计类型
                alert_type = alert['type']
                type_counts[alert_type] = type_counts.get(alert_type, 0) + 1
                
                # 收集最近的高危警报
                if alert['level'] == 'high':
                    recent_high_threats.append(alert)
            
            # 只保留最近的5个高危警报
            recent_high_threats.sort(key=lambda x: x['timestamp'], reverse=True)
            recent_high_threats = recent_high_threats[:5]
            
            return {
                'total_alerts': len(self.alert_history),
                'alerts_by_level': level_counts,
                'alerts_by_type': type_counts,
                'recent_high_threats': recent_high_threats,
                'known_malicious_ips': len(self.known_malicious_ips),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Failed to get threat summary: {str(e)}")
            return {} 