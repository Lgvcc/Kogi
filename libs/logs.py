#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/7/30 10:28 
# @Author : mingyang.liang
# @Site :  
# @File : logs.py 
# @Software: PyCharm

# coding:utf-8
import os
import logging.handlers


def get_logger(log_name):
    # 判断当前目录log目录是否存在，不存在则创建
    if not os.path.isdir("log/"):
        try:
            os.makedirs("log/")
        except Exception as e:
            print("Can not create dir:", e)


    # 日志设置
    log_file = 'log/%s.log' % log_name

    handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)

    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

    formatter = logging.Formatter(fmt)  # 实例化formatter
    handler.setFormatter(formatter)  # 为handler添加formatter
    logger = logging.getLogger('%s_log' % log_name)
    logger.addHandler(handler)  # 为logger添加handler
    logger.setLevel(logging.INFO)  # 设置存入文件的log等级
    return logger