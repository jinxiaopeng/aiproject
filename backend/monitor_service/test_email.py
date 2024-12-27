import yagmail

# 邮箱配置
smtp_username = '3526357160@qq.com'
smtp_password = 'hmvpvaizamnkdaaj'
to_email = '3526357160@qq.com'

try:
    print("初始化邮件客户端...")
    # 初始化yagmail SMTP客户端
    yag = yagmail.SMTP(user=smtp_username, 
                      password=smtp_password, 
                      host='smtp.qq.com')
    
    print("正在发送邮件...")
    # 发送邮件
    yag.send(to=to_email,
             subject='测试邮件',
             contents='这是一封测试邮件，用于测试SMTP连接。')
    
    print("邮件发送成功！")
    
except Exception as e:
    print(f"发送失败: {str(e)}")
finally:
    try:
        yag.close()
    except:
        pass 