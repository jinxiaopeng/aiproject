import psutil
import logging
from typing import Dict, List
import socket
from datetime import datetime
import netifaces
import struct
from scapy.all import sniff, IP

class NetworkCollector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._initialize()
        self.connection_history = {}
        self.packet_buffer = []
        self.suspicious_ips = set()

    def _initialize(self):
        """初始化网络收集器"""
        try:
            # 获取本机网络接口
            self.interfaces = netifaces.interfaces()
            # 获取本机IP
            self.host_ip = socket.gethostbyname(socket.gethostname())
            self.logger.info(f"Network collector initialized for {self.host_ip}")
        except Exception as e:
            self.logger.error(f"Failed to initialize network collector: {str(e)}")
            self.host_ip = "0.0.0.0"

    async def collect_network_data(self) -> Dict:
        """收集网络数据"""
        try:
            # 基础网络统计
            net_io = psutil.net_io_counters()
            
            # 获取网络连接信息
            connections = self._get_active_connections()
            
            # 分析网络流量模式
            traffic_pattern = self._analyze_traffic_pattern()
            
            # 检测可疑连接
            suspicious = self._detect_suspicious_connections(connections)
            
            return {
                'timestamp': datetime.now().isoformat(),
                'basic_stats': {
                    'bytes_sent': net_io.bytes_sent,
                    'bytes_recv': net_io.bytes_recv,
                    'packets_sent': net_io.packets_sent,
                    'packets_recv': net_io.packets_recv,
                    'errin': net_io.errin,
                    'errout': net_io.errout,
                    'dropin': net_io.dropin,
                    'dropout': net_io.dropout
                },
                'connections': connections,
                'traffic_pattern': traffic_pattern,
                'suspicious_activity': suspicious,
                'interfaces': self._get_interface_stats()
            }
        except Exception as e:
            self.logger.error(f"Failed to collect network data: {str(e)}")
            return {}

    def _get_active_connections(self) -> List[Dict]:
        """获取活动的网络连接"""
        connections = []
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'ESTABLISHED':
                    connection_info = {
                        'local_ip': conn.laddr.ip,
                        'local_port': conn.laddr.port,
                        'remote_ip': conn.raddr.ip if conn.raddr else None,
                        'remote_port': conn.raddr.port if conn.raddr else None,
                        'status': conn.status,
                        'pid': conn.pid
                    }
                    connections.append(connection_info)
                    
                    # 记录连接历史
                    if conn.raddr:
                        key = f"{conn.raddr.ip}:{conn.raddr.port}"
                        if key not in self.connection_history:
                            self.connection_history[key] = {
                                'first_seen': datetime.now(),
                                'count': 1
                            }
                        else:
                            self.connection_history[key]['count'] += 1
                            
        except Exception as e:
            self.logger.error(f"Failed to get active connections: {str(e)}")
        return connections

    def _analyze_traffic_pattern(self) -> Dict:
        """分析流量模式"""
        try:
            # 分析连接频率
            connection_frequency = {}
            for key, value in self.connection_history.items():
                if (datetime.now() - value['first_seen']).seconds < 3600:  # 最近一小时
                    connection_frequency[key] = value['count']

            # 识别高频连接
            high_frequency = {k: v for k, v in connection_frequency.items() 
                            if v > 100}  # 每小时超过100次的连接

            return {
                'high_frequency_connections': high_frequency,
                'total_active_connections': len(self.connection_history),
                'recent_connections': len(connection_frequency)
            }
        except Exception as e:
            self.logger.error(f"Failed to analyze traffic pattern: {str(e)}")
            return {}

    def _detect_suspicious_connections(self, connections: List[Dict]) -> List[Dict]:
        """检测可疑连接"""
        suspicious = []
        try:
            for conn in connections:
                if conn['remote_ip']:
                    # 检查是否是已知的可疑IP
                    if conn['remote_ip'] in self.suspicious_ips:
                        suspicious.append({
                            'ip': conn['remote_ip'],
                            'port': conn['remote_port'],
                            'reason': 'Known suspicious IP'
                        })
                    
                    # 检查异常端口
                    if conn['remote_port'] in [22, 23, 3389]:  # 远程访问端口
                        suspicious.append({
                            'ip': conn['remote_ip'],
                            'port': conn['remote_port'],
                            'reason': 'Remote access port'
                        })
                    
                    # 检查连接频率
                    key = f"{conn['remote_ip']}:{conn['remote_port']}"
                    if key in self.connection_history:
                        if self.connection_history[key]['count'] > 100:
                            suspicious.append({
                                'ip': conn['remote_ip'],
                                'port': conn['remote_port'],
                                'reason': 'High frequency connection'
                            })
        except Exception as e:
            self.logger.error(f"Failed to detect suspicious connections: {str(e)}")
        return suspicious

    def _get_interface_stats(self) -> Dict:
        """获取网络接口统计信息"""
        stats = {}
        try:
            for interface in self.interfaces:
                try:
                    addrs = netifaces.ifaddresses(interface)
                    if netifaces.AF_INET in addrs:
                        stats[interface] = {
                            'ip': addrs[netifaces.AF_INET][0]['addr'],
                            'netmask': addrs[netifaces.AF_INET][0]['netmask']
                        }
                        # 获取接口流量统计
                        if interface in psutil.net_io_counters(pernic=True):
                            nic_stats = psutil.net_io_counters(pernic=True)[interface]
                            stats[interface].update({
                                'bytes_sent': nic_stats.bytes_sent,
                                'bytes_recv': nic_stats.bytes_recv,
                                'packets_sent': nic_stats.packets_sent,
                                'packets_recv': nic_stats.packets_recv
                            })
                except Exception as e:
                    self.logger.error(f"Failed to get stats for interface {interface}: {str(e)}")
        except Exception as e:
            self.logger.error(f"Failed to get interface stats: {str(e)}")
        return stats

    def packet_callback(self, packet):
        """数据包回调函数"""
        try:
            if IP in packet:
                self.packet_buffer.append({
                    'time': datetime.now(),
                    'src': packet[IP].src,
                    'dst': packet[IP].dst,
                    'proto': packet[IP].proto,
                    'size': len(packet)
                })
                
                # 保持缓冲区大小
                if len(self.packet_buffer) > 1000:
                    self.packet_buffer.pop(0)
        except Exception as e:
            self.logger.error(f"Failed to process packet: {str(e)}")

    def start_packet_capture(self):
        """开始数据包捕获"""
        try:
            sniff(prn=self.packet_callback, store=0)
        except Exception as e:
            self.logger.error(f"Failed to start packet capture: {str(e)}")

    def analyze_packet_flow(self) -> Dict:
        """分析数据包流"""
        try:
            if not self.packet_buffer:
                return {}

            # 计算流量统计
            total_size = sum(p['size'] for p in self.packet_buffer)
            protocols = {}
            sources = {}
            destinations = {}

            for packet in self.packet_buffer:
                # 统计协议
                proto = packet['proto']
                protocols[proto] = protocols.get(proto, 0) + 1

                # 统计源IP
                src = packet['src']
                sources[src] = sources.get(src, 0) + 1

                # 统计目标IP
                dst = packet['dst']
                destinations[dst] = destinations.get(dst, 0) + 1

            return {
                'total_packets': len(self.packet_buffer),
                'total_size': total_size,
                'protocols': protocols,
                'top_sources': dict(sorted(sources.items(), key=lambda x: x[1], reverse=True)[:5]),
                'top_destinations': dict(sorted(destinations.items(), key=lambda x: x[1], reverse=True)[:5])
            }
        except Exception as e:
            self.logger.error(f"Failed to analyze packet flow: {str(e)}")
            return {} 