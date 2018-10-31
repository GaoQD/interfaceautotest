# -*- coding: utf-8 -*-
# @Time    : 10:43
# @Author  : Administor
# @File    : send_Email.py
# @Software: PyCharm

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import time

def send_email(now_time):
    sender = 'cap4819@126.com'
    receivers = 'gaoqiangde@dohia.com'
    password = 'gao367985'

    try:
        msg = MIMEMultipart()
        msg['From'] = sender
        # msg['To'] = ';'.join(receivers)
        msg['To'] = receivers
        msg['Subject'] = '接口测试报告'

        # htmlf = open('..\\report\\' + now_time + '.html', 'rb')
        # htmlcont = htmlf.read()
        # email_text = MIMEText(htmlcont, 'html', 'utf-8')
        # msg.attach(email_text)
        sep = os.sep
        # attname = '..\\report\\' + now_time + '.html'.split(sep)[-1]
        # email_att = MIMEApplication(open('..\\report\\' + now_time + '.html', 'rb').read())
        # email_att.add_header('Content-Disposition', 'attachment', filename=attname)
        attname1 = '..\\log\\test.log'.split(sep)[-1]
        email_att1 = MIMEApplication(open('..\\log\\test.log', 'rb').read())
        email_att1.add_header('Content-Disposition', 'attachment', filename=attname1)
        # msg.attach(email_att)
        msg.attach(email_att1)

        smtpObj = smtplib.SMTP('smtp.126.com',25)
        smtpObj.set_debuglevel(1)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(sender,password)
        smtpObj.sendmail(sender,receivers,msg.as_string())
        smtpObj.quit()
        print('邮件发送成功~')
    except Exception as ex:
        print('Error: 无法发送邮件',ex)