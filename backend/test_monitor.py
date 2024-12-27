import requests
import json
from datetime import datetime, timedelta

class MonitorSystemTester:
    def __init__(self):
        self.base_url = "http://localhost:3017"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer YOUR_TOKEN_HERE"  # 需要替换为实际的token
        }

    def test_monitor_stats(self):
        """测试监控统计数据接口"""
        url = f"{self.base_url}/api/monitor/stats"
        try:
            response = requests.get(url, headers=self.headers)
            print(f"\n请求URL: {url}")
            print(f"响应状态码: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print("\n=== 监控统计数据 ===")
                print(f"登录预警: {data.get('loginAlerts', 0)} (待处理: {data.get('loginPending', 0)}, 已处理: {data.get('loginHandled', 0)})")
                print(f"操作预警: {data.get('operationAlerts', 0)} (待处理: {data.get('operationPending', 0)}, 已处理: {data.get('operationHandled', 0)})")
                print(f"安全预警: {data.get('securityAlerts', 0)} (待处理: {data.get('securityPending', 0)}, 已处理: {data.get('securityHandled', 0)})")
                print("✅ 监控统计数据获取成功")
                return True
            else:
                print(f"❌ 监控统计数据获取失败: {response.status_code}")
                try:
                    print(f"错误详情: {response.text}")
                except:
                    pass
                return False
        except Exception as e:
            print(f"❌ 监控统计数据请求异���: {str(e)}")
            return False

    def test_monitor_settings(self):
        """测试监控设置接口"""
        url = f"{self.base_url}/api/monitor/settings"
        try:
            print(f"\n请求URL: {url}")
            response = requests.get(url, headers=self.headers)
            print(f"响应状态码: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print("\n=== 监控设置 ===")
                print(f"CPU使用率阈值: {data['thresholds']['cpu_usage']}%")
                print(f"内存使用率阈值: {data['thresholds']['memory_usage']}%")
                print(f"磁盘使用率阈值: {data['thresholds']['disk_usage']}%")
                print(f"网络延迟阈值: {data['thresholds']['network_latency']}ms")
                print("\n通知设置:")
                print(f"邮件通知: {'启用' if data['notification']['email'] else '禁用'}")
                print(f"Slack通知: {'启用' if data['notification']['slack'] else '禁用'}")
                print(f"Webhook通知: {'启用' if data['notification']['webhook'] else '禁用'}")
                print("\n告警规则:")
                for rule in data['alert_rules']:
                    print(f"- {rule['name']} ({rule['severity']}): {rule['condition']}")
                print("✅ 监控设置获取成功")
                return True
            else:
                print(f"❌ 监控设置获取失败: {response.status_code}")
                try:
                    print(f"错误详情: {response.text}")
                except:
                    pass
                return False
        except Exception as e:
            print(f"❌ 监控设置请求异常: {str(e)}")
            return False

    def test_alert_list(self):
        """测试预警列表接口"""
        url = f"{self.base_url}/api/monitor/alerts"
        params = {
            "page": 1,
            "pageSize": 10
        }
        try:
            print(f"\n请求URL: {url}")
            print(f"请求参数: {params}")
            response = requests.get(url, headers=self.headers, params=params)
            print(f"响应状态码: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print("\n=== 预警列表 ===")
                for alert in data:
                    print(f"- [{alert['type']}] {alert['message']} ({alert['status']})")
                print("✅ 预警列表获取成功")
                return True
            else:
                print(f"❌ 预警列表获取失败: {response.status_code}")
                try:
                    print(f"错误详情: {response.text}")
                except:
                    pass
                return False
        except Exception as e:
            print(f"❌ 预警列表请求异常: {str(e)}")
            return False

    def run_all_tests(self):
        """运行所有测试"""
        print("\n=== 开始测试监控预警系统 ===")
        print(f"基础URL: {self.base_url}")
        
        tests = [
            self.test_monitor_stats,
            self.test_monitor_settings,
            self.test_alert_list
        ]
        
        results = [test() for test in tests]
        total = len(results)
        passed = sum(results)
        
        print("\n=== 测试结果汇总 ===")
        print(f"总计: {total} 个测试")
        print(f"通过: {passed} 个")
        print(f"失败: {total - passed} 个")
        print(f"通过率: {(passed/total*100):.2f}%")

if __name__ == "__main__":
    tester = MonitorSystemTester()
    tester.run_all_tests()