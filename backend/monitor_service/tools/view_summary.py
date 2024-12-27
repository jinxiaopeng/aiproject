import os
import json
import sys
from datetime import datetime
import click
from typing import Dict, List
import pandas as pd
from tabulate import tabulate
import colorama
from colorama import Fore, Style

# 初始化colorama
colorama.init()

class ThreatSummaryViewer:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.summary_file = os.path.join(self.data_dir, 'threat_summary.json')
        self.threats_file = os.path.join(self.data_dir, 'threats.json')

    def load_summary(self) -> Dict:
        """加载威胁摘要"""
        try:
            if os.path.exists(self.summary_file):
                with open(self.summary_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading summary: {str(e)}")
            return {}

    def load_threats(self) -> List[Dict]:
        """加载威胁记录"""
        try:
            if os.path.exists(self.threats_file):
                with open(self.threats_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading threats: {str(e)}")
            return []

    def display_summary(self):
        """显示威胁摘要"""
        summary = self.load_summary()
        if not summary:
            print(f"{Fore.YELLOW}No threat summary available{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}=== Threat Summary ==={Style.RESET_ALL}")
        print(f"Last updated: {summary.get('timestamp', 'Unknown')}")
        print(f"Total alerts: {summary.get('total_alerts', 0)}")
        print(f"Known malicious IPs: {summary.get('known_malicious_ips', 0)}")

        # 显示按级别统计
        if 'alerts_by_level' in summary:
            print(f"\n{Fore.CYAN}Alerts by Level:{Style.RESET_ALL}")
            level_data = []
            for level, count in summary['alerts_by_level'].items():
                color = {
                    'high': Fore.RED,
                    'medium': Fore.YELLOW,
                    'low': Fore.GREEN,
                    'warning': Fore.BLUE
                }.get(level.lower(), '')
                level_data.append([f"{color}{level}{Style.RESET_ALL}", count])
            print(tabulate(level_data, headers=['Level', 'Count'], tablefmt='grid'))

        # 显示按类型统计
        if 'alerts_by_type' in summary:
            print(f"\n{Fore.CYAN}Alerts by Type:{Style.RESET_ALL}")
            type_data = [[type_, count] for type_, count in summary['alerts_by_type'].items()]
            print(tabulate(type_data, headers=['Type', 'Count'], tablefmt='grid'))

        # 显示最近的高危威胁
        if 'recent_high_threats' in summary and summary['recent_high_threats']:
            print(f"\n{Fore.RED}Recent High-Level Threats:{Style.RESET_ALL}")
            threats_data = []
            for threat in summary['recent_high_threats']:
                threats_data.append([
                    threat.get('timestamp', 'Unknown'),
                    threat.get('type', 'Unknown'),
                    threat.get('description', 'No description'),
                    threat.get('source_ip', 'N/A')
                ])
            print(tabulate(threats_data, 
                         headers=['Timestamp', 'Type', 'Description', 'Source IP'],
                         tablefmt='grid'))

    def display_threats(self, level: str = None, limit: int = 10):
        """显示威胁记录"""
        threats = self.load_threats()
        if not threats:
            print(f"{Fore.YELLOW}No threats recorded{Style.RESET_ALL}")
            return

        # 过滤威胁
        if level:
            threats = [t for t in threats if t.get('level', '').lower() == level.lower()]

        # 限制显示数量
        threats = threats[-limit:]

        print(f"\n{Fore.CYAN}=== Recent Threats {'(' + level.upper() + ')' if level else ''} ==={Style.RESET_ALL}")
        
        threats_data = []
        for threat in threats:
            level_color = {
                'high': Fore.RED,
                'medium': Fore.YELLOW,
                'low': Fore.GREEN,
                'warning': Fore.BLUE
            }.get(threat.get('level', '').lower(), '')
            
            threats_data.append([
                threat.get('timestamp', 'Unknown'),
                f"{level_color}{threat.get('level', 'Unknown')}{Style.RESET_ALL}",
                threat.get('type', 'Unknown'),
                threat.get('description', 'No description'),
                threat.get('source_ip', 'N/A')
            ])
        
        print(tabulate(threats_data,
                      headers=['Timestamp', 'Level', 'Type', 'Description', 'Source IP'],
                      tablefmt='grid'))

    def export_to_csv(self, output_file: str):
        """导出威胁记录到CSV文件"""
        threats = self.load_threats()
        if not threats:
            print(f"{Fore.YELLOW}No threats to export{Style.RESET_ALL}")
            return

        try:
            df = pd.DataFrame(threats)
            df.to_csv(output_file, index=False)
            print(f"{Fore.GREEN}Successfully exported threats to {output_file}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export threats: {str(e)}{Style.RESET_ALL}")

@click.group()
def cli():
    """网络安全监控系统 - 威胁查看工具"""
    pass

@cli.command()
def summary():
    """显示威胁摘要"""
    viewer = ThreatSummaryViewer()
    viewer.display_summary()

@cli.command()
@click.option('--level', type=click.Choice(['high', 'medium', 'low', 'warning'], case_sensitive=False),
              help='Filter threats by level')
@click.option('--limit', type=int, default=10, help='Number of threats to display')
def threats(level, limit):
    """显示威胁记录"""
    viewer = ThreatSummaryViewer()
    viewer.display_threats(level, limit)

@cli.command()
@click.argument('output_file', type=click.Path())
def export(output_file):
    """导出威胁记录到CSV文件"""
    viewer = ThreatSummaryViewer()
    viewer.export_to_csv(output_file)

if __name__ == '__main__':
    try:
        cli()
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1) 