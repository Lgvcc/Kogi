#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/7/30 9:58 
# @Author : mingyang.liang
# @Site :  
# @File : send_task.py 
# @Software: PyCharm
import urllib3

urllib3.disable_warnings()
import json
import pinyin
import unicodedata

from web_requests.web_requests import WebRequests
from libs.redis_queue import RedisQueue

headers = {
    'Accept-Encoding': 'br, gzip, deflate',
    'Accept-Language': 'zh-cn',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.5(0x17000523) NetType/WIFI Language/zh_CN',
    'Referer': 'https://servicewechat.com/wx3a113f35a7239658/124/page-frame.html',
    'token': 'token:1a06fc70c94a315ede175e446f9d9557'
}

req = WebRequests()

prefix_url = 'https://api.kogi.club'

"""
url 示例 https://api.kogi.club/merchandise/search?page=1&typeId=&brandId=462&order=2&size=&state=&status=-1
"""


def get_all_brand():
    url = prefix_url + '/classify/brand/withlogo'
    r = req.get(url, headers=headers, verify=False)
    if r is None:
        return None
    content = r.content.decode('utf-8')
    dict_data = json.loads(content)
    print(dict_data)
    datas = dict_data['data']
    brand_list = []
    for data in datas:
        item = {}
        item['brand_id'] = data['id']
        item['brand_img_url'] = data['image']
        item['brand_name'] = data['name']
        brand_name_pinyin = data['pinyin']
        if not brand_name_pinyin:
            # print(item['brand_name'], '---------------------------------------')
            my_str = pinyin.get(item['brand_name'])
            res = unicodedata.normalize('NFKD', my_str).encode('ascii', 'ignore')
            brand_name_pinyin = res.decode('utf-8')
            # print(brand_name_pinyin)
        item['brand_name_pinyin'] = brand_name_pinyin
        print('商品id: ', item['brand_id'], '商品名称: ', item['brand_name'], '商品名称(拼音): ', item['brand_name_pinyin'],
              '商品图片url: ',
              item['brand_img_url'])
        brand_list.append(item)
    return brand_list


def get_brand_url(brand_list):
    """ 获取品牌 商品的总数量"""
    url_lists = []
    for data in brand_list:
        item = {}
        brand_name_pinyin = data['brand_name_pinyin']
        brandId = data['brand_id']
        url_list = get_total_page(brandId, brand_name_pinyin)
        item[brand_name_pinyin] = url_list
        url_lists.append(item)
    return url_lists


def get_total_page(brandId, brand_name_pinyin):
    """
     #  https://api.kogi.club/merchandise/search?page=1&typeId=&brandId=462&order=2&size=&state=&status=-1
    :param brandId:
    :param brand_name_pinyin:
    :return:
    """
    # print(brandId, brand_name_pinyin)
    url = 'https://api.kogi.club/merchandise/search?page=1&typeId=&brandId=%s&order=2&size=&state=&status=-1' % brandId

    r = req.get(url, headers=headers, verify=False)
    content = r.content.decode('utf-8')
    dict_data = json.loads(content)
    datas = dict_data.get('data')
    total = datas['count']
    page_size = datas['pageSize']
    print(total, page_size)
    if total % page_size == 0:
        total_page = total // page_size
    else:
        total_page = total // page_size + 1
    start_url = 'https://api.kogi.club/merchandise/search?page=%s&typeId=&brandId=' + str(
        brandId) + '&order=2&size=&state=&status=-1'
    print(total_page)
    url_list = [start_url % str(pageNo) for pageNo in range(1, total_page + 1)]
    return url_list


def send_urls(brand_name, url_list):
    queue = RedisQueue(brand_name)
    for url in url_list:
        queue.put(url)


def get_all_url():
    # 1.获取所有品牌的分类 以及id
    brand_list = get_all_brand()

    # 2.根据品牌信息 获取品牌总商品数量 和 总页数

    url_list = get_brand_url(brand_list)
    # get_total_page(brand_url_list)
    return url_list


def main():
    get_all_url()


if __name__ == '__main__':
    main()
