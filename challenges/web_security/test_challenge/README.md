# SQL注入基础训练

这是一个基础的SQL注入训练靶场，帮助你理解SQL注入的原理和防御方法。

## 学习目标

1. 理解SQL注入的基本原理
2. 掌握基本的SQL注入技术
3. 学习SQL注入的防御方法

## 环境要求

- Python 3.8+
- Flask 2.0.1
- SQLite3

## 快速开始

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 启动应用：
```bash
python app.py
```

3. 访问应用：
```
http://localhost:3000
```

## 训练步骤

1. 环境准备
   - 启动靶场环境
   - 访问Web应用

2. 漏洞发现
   - 观察登录表单的行为
   - 尝试输入特殊字符
   - 分析应用的响应

3. 漏洞利用
   - 构造SQL注入payload
   - 绕过登录验证
   - 获取flag

## 提示

1. 尝试在用户名输入框中使用单引号
2. 考虑使用OR 1=1绕过登录验证
3. 观察应用的错误信息

## 注意事项

1. 请不要使用自动化工具
2. 完成后请及时提交flag
3. 遵守实验规则，不要攻击其他用户

## 参考资料

1. [SQL注入基础](https://www.w3schools.com/sql/sql_injection.asp)
2. [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
3. [SQL注入防御指南](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) 