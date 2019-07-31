#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/7/30 9:58
# @Author : mingyang.liang
# @Site :
# @File : spider.py
# @Software: PyCharm
import json
import csv
import os
from datetime import datetime

from web_requests.web_requests import WebRequests
import send_task
from send_email import send_email_annex

req = WebRequests()
headers = {
    'Accept-Encoding': 'br, gzip, deflate',
    'Accept-Language': 'zh-cn',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.5(0x17000523) NetType/WIFI Language/zh_CN',
    'Referer': 'https://servicewechat.com/wx3a113f35a7239658/124/page-frame.html',
    'token': 'token:1a06fc70c94a315ede175e446f9d9557'
}


class KoGi(object):
    def __init__(self):
        self.page = 1
        self.url_list = []
        self.prefix_url = 'https://api.kogi.club'

    def ready_url_list(self):

        return send_task.get_all_url()

    def parse_html(self, r):
        content = r.content.decode('utf-8')
        datas = json.loads(content)
        data = datas['data']
        goods_list = data['list']
        data_list = []
        for goods_dict in goods_list:
            # print(goods_dict)
            item = {}
            """{'id': 75284, 'image': 'http://image.kogi.club/FjRvbzktFnhsm6REp587RIiFLekb', 'userId': 18084, 'headimg': 'https://hd.kogi.club/headimg/18084/my_upload_headimg1563599201918.jpg?imageView2/3/w/264/h/264/q/100|imageslim', 'name': '& Other Stories蓝色圆领无袖修身连衣裙', 'describe': '蓝色圆领无袖修身连衣裙', 'lable': None, 'status': 0, 'sizeName': '160/80A', 'kogiSizeName': 'S', 'brandName': '& Other Stories', 'colorName': None, 'price': 129.0, 'originalPrice': 599.0, 'hangtag': False, 'userName': '媛媛张', 'job': '', 'height': None, 'upperSize': 'XS,S', 'bottomSize': 'XS,S,25,26', 'lend': -1, 'endTime': None, 'firstImage': 'FjRvbzktFnhsm6REp587RIiFLekb', 'state': 3, 'stock': 0, 'online': 1, 'sizeId': 12, 'kogiSizeId': 2, 'brandId': 6, 'typeId': 2, 'activityPrice': None, 'canRefund': None}"""
            id = goods_dict['id']
            url = self.prefix_url + '/merchandise/detail?id=%s' % str(id)
            res = req.get(url, headers=headers, verify=False)
            if res is None: continue
            content = res.content.decode('utf-8')
            dict_data = json.loads(content)
            data = dict_data['data']
            item['goods_id'] = data.get('id')
            item['user_id'] = data.get('userId')
            user_name = data.get('userName')
            item['user_name'] = user_name
            goods_name = data.get('describe')
            item['goods_name'] = goods_name
            brand_name = data.get('brandName')
            item['brand_name'] = brand_name
            item['goods_price'] = data.get('price')
            item['original_price'] = data.get('originalPrice')
            status = data.get('status')
            # print(data)
            if status:
                status = False
            else:
                status = True  # True 下架
            item['goods_status'] = status
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), item)

            data_list.append(item)

        return data_list

    def process_item(self):
        pass

    def save_item(self, content_list):
        brand_name = content_list[0]['brand_name']
        import os
        if os.path.exists('./Data'):
            print('文件存在')
            pass
        else:
            os.mkdir('./Data')

        file_path = './Data/' + 'brand_list.csv'
        csvFile = open(file_path, "a+")  # 创建csv文件
        writer = csv.writer(csvFile)  # 创建写的对象
        # 先写入columns_name
        colos = ['当前时间', '商品id', '商品名称', '用户id', '用户名称', '商品品牌', '商品价格', '商品原价', '是否下架']
        writer.writerow(colos)  # 写入列的名称
        for content in content_list:
            goods_list = []
            created_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            goods_list.append(created_time)
            goods_list.append(content.get('goods_id'))
            goods_list.append(content.get('goods_name'))
            goods_list.append(content.get('user_id'))
            goods_list.append(content.get('user_name'))
            goods_list.append(content.get('brand_name'))
            goods_list.append(content.get('goods_price'))
            goods_list.append(content.get('original_price'))
            goods_list.append(content.get('goods_status'))
            # 写入多行用writerows                                #写入多行
            writer.writerow(goods_list)
        csvFile.close()
        pass

    def run(self):
        # 1.获取所有的品牌和url
        data_list = self.ready_url_list()
        for data in data_list:  # dict
            for brand_name, url_list in data.items():
                print(brand_name, url_list)
                content_list = []
                for url in url_list:
                    r = req.get(url, headers=headers, verify=False)
                    if r is None: continue
                    goods_list = self.parse_html(r)
                    content_list += goods_list
                # print(content_list)
                print(len(content_list))
                print(content_list)
                # 开始写入csv文件
                self.save_item(content_list)

        # 数据整理完毕

        # 发送数据到邮箱
        send_email_annex('./Data', './Data.zip', '可及品牌数据')


if __name__ == '__main__':
    kg = KoGi()
    kg.run()
