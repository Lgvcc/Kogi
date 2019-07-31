#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/7/30 14:55
# @Author : mingyang.liang
# @Site :
# @File : send_email.py
# @Software: PyCharm
# coding:utf-8
import os
import shutil
import zipfile
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def zipDir(dirpath, outFullName):
    '''
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName:  压缩文件保存路径+XXXX.zip
    :return: 无
    '''
    zip = zipfile.ZipFile(outFullName, 'w', zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标和路径，只对目标文件夹下边的文件及文件夹进行压缩（包括父文件夹本身）
        this_path = os.path.abspath('.')
        fpath = path.replace(this_path, '')
        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()


def send_email_annex(open_annex_name, email_annex_name, annex_title):
    """ 发送附件 """
    zipDir(open_annex_name, email_annex_name)
    # 创建一个带附件的实例
    msg = MIMEMultipart()

    # 构造附件2
    att2 = MIMEText(open(email_annex_name, 'rb').read(), 'base64', 'gb2312')
    att2["Content-Type"] = 'application/octet-stream'
    att2["Content-Disposition"] = 'attachment; filename="{}"'.format(email_annex_name)
    msg.attach(att2)

    receiver = os.environ.get('EMAIL_TO')
    receiver = receiver.split(',')
    receiver = ';'.join(receiver)
    # print(receiver)
    # 加邮件头
    msg['to'] = receiver
    msg['from'] = os.environ.get('MAIL_USER')
    msg['subject'] = annex_title
    smtpserver = os.environ.get('MAIL_HOST')
    user = os.environ.get('MAIL_USER')
    password = os.environ.get('MAIL_PASS')
    port = os.environ.get('MAIL_PORT')
    # 发送邮件
    try:
        server = smtplib.SMTP()
        server.connect(smtpserver, port=port)
        server.login(user, password)  # XXX为用户名, XXXXX为密码
        server.sendmail(msg['from'], receiver.split(';'), msg.as_string())
        server.quit()
        print('附件发送成功')
    except Exception as e:
        print(e)
        print("附件发送失败")
    if os.path.exists('./Data.zip'):  # 如果文件存在
        # 删除文件，可使用以下两种方法。
        os.remove('./Data.zip')
        print('文件夹已经删除')
        # os.unlink(path)
    else:
        print('文件不存在')  # 则返回文件不存在

    if os.path.exists('./Data'):
        print('文件---------------------')
        shutil.rmtree('./Data')
        # os.mkdir('./Data')
    else:
        print('文件夹不存在')



if __name__ == '__main__':
    # open_annex_name 打开文件的名称
    # email_annex_name 发送附件的名称
    # annex_title 附件的标题
    send_email_annex('./Data', './Data.zip', '测试标题')