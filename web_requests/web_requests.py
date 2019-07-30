#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 2019/7/30 9:59 
# @Author : mingyang.liang
# @Site :  
# @File : web_requests.py
# @Software: PyCharm
import requests
import traceback

from libs.logs import get_logger

logger = get_logger('web_requests')


class WebRequests(object):

    def __init__(self, **kwargs):
        self.session = requests.Session()
        self.requests = requests

    def _requests_helper(self, method_name, url, **kwargs):
        retry_time = 1
        timeout = kwargs.get('timeout')
        if timeout is None:
            timeout = 120
        headers = kwargs.get('headers')
        fail = 0
        res = None
        while fail < 5:
            try:
                res = self.session.request(method_name, url, **kwargs)
                # print(res.status_code, '---')
                if res.status_code == requests.codes.ok:
                    logger.info('*' * 20 + '请求成功: status_code: %s' % res.status_code + '*' * 20)
                    break
                else:
                    raise requests.RequestException
            except Exception as e:
                logger.info('*' * 20 + '网络异常' + '*' * 20)
                err = traceback.format_exc()
                logger.info(err)
        return res

    def get(self, url, **kwargs):
        return self._requests_helper('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self._requests_helper('POST', url, **kwargs)
