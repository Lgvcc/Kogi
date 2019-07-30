#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 2019/7/30 9:59 
# @Author : mingyang.liang
# @Site :  
# @File : web_requests.py
# @Software: PyCharm
import requests


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
        while fail < 5:
            try:
                res = self.session.request(method_name, url, **kwargs)
                print(res.status_code, '---')
                if res.status_code == requests.codes.ok:
                    break
                else:
                    raise requests.RequestException
            except Exception as e:
                print('网络异常: ')



    def get(self, url, **kwargs):
        return self._requests_helper('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self._requests_helper('POST', url, **kwargs)
