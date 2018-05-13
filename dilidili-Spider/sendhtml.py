import smtplib
import logging
import time
import datetime
from email.mime.text import MIMEText
from email.header import Header

def send():
    sender = '发件邮箱'
    pwd = '密码'
    receivers = ['收件邮箱']

    with open('result.html', 'rb') as f:
        mail_msg = f.read()

    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header('每日番剧推送', 'utf-8')
    message['To'] = Header('horizon', 'utf-8')
    message['Subject'] = Header('今日番剧', 'utf-8')

    logging.basicConfig(filename='program.log', level=logging.INFO)
    try:
        server = smtplib.SMTP_SSL('SMTP服务器地址', 端口号)
        server.login(sender, pwd)
        server.sendmail(sender, receivers, message.as_string())
        logging.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '：邮件发送成功！')
    except smtplib.SMTPException:

        logging.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '：邮件发送失败,一分钟后尝试重新发送！')
        time.sleep(60)
        try:
            server.sendmail(sender, receivers, message.as_string())
        except smtplib.SMTPException:
            logging.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '：邮件发送失败！' + str(smtplib.SMTPException))

