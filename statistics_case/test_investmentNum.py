# -*- coding: utf-8 -*-
# @Time    : 10:11
# @Author  : Administor
# @File    : test_investmentNum.py
# @Software: PyCharm
import unittest
from common.common import *
from statistics_case.test_Login import test_Login
import json
import requests
from config.readConfig import read_config
import time

class test_investmentNum(unittest.TestCase):
    @classmethod
    def setUp(self):
        pass

    s = requests.session()
    '''
     @Description:当日投资用户数
    '''
    def test_investment_num(self):
        url = "https://jr.huanqiu.com/set-cookie/?key=version-grey&val=pre"
        l = self.s.get(url)
        platform_statistics = read_config().get_string('pre_h5','platform_statistics')
        order_count = read_config().get_string('pre_online','order_count')
        users_statistics = read_config().get_string('pre_online','users_statistics')
        query_orders = read_config().get_string('pre_online','query_orders')
        file_name = "当日投资用户数"
        file_path = '..\\testStatistics\\' + file_name + '.xls'
        copy_file(file_name)
        write_xls_time('2018-07-15', file_path)
        xls_list = get_xls(file_path)
        for i in range(1,len(xls_list)):
            start_time = xls_list[i]['开始时间']
            end_time = xls_list[i]['结束时间']
            param_time = time.strftime('%Y-%m-%d', time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
            r = self.s.get(
                platform_statistics + str(param_time),
                json={"Content-Type": "application/json;charset=UTF-8", "huanqiu_backend_session": test_Login.test_login(self,'pre_h5')}
            )
            json_dict = json.loads(r.text)
            '''
             @Description:H5 当日投资用户数
            '''
            h5_sum_name_now = json_dict['data']['sum_name_now']
            write_xls(i + 1, 2, float(h5_sum_name_now), file_path)

            '''
             @Description:订单统计--购买总人数
            '''
            pageNO = 1
            order = self.s.get(
                str(order_count) + str(pageNO) + '&channel=&date=' + str(start_time) + '|' + str(end_time),
                json={"Content-Type": "application/json;charset=UTF-8", "session": test_Login.test_login(self,'pre_online')}
            )
            json_dict_order = json.loads(order.text)
            if json_dict_order['data']['total'] > 10:
                ord = self.s.get(
                    str(order_count) + str(pageNO + int(json_dict_order['data']['total']/11)) + '&channel=&date=' + str(start_time) + '|' + str(end_time),
                    json={"Content-Type": "application/json;charset=UTF-8", "session": test_Login.test_login(self,'pre_online')}
                )
                json_dict_ord = json.loads(ord.text)
                acc = json_dict_ord['data']['data'][len(json_dict_ord['data']['data']) - 1]
                write_xls(i + 1, 3, float(acc['people_sum']), file_path)
            else:
                account = json_dict_order['data']['data'][len(json_dict_order['data']['data']) - 1]
                write_xls(i + 1, 3, float(account['people_sum']), file_path)
            '''
             @Description:用户统计--当日购买总人数
            '''
            user = self.s.get(
                str(users_statistics) + str(start_time) + '|' + str(end_time),
                json={"Content-Type": "application/json;charset=UTF-8", "session": test_Login.test_login(self,'pre_online')}
            )
            json_dict_user = json.loads(user.text)
            for j in json_dict_user['data']['用户情况']:
                write_xls(i + 1, 4, float(j['users']), file_path)

            query = self.s.get(
                str(query_orders) + str(start_time) + '|' + str(end_time),
                json={"Content-Type": "application/json;charset=UTF-8","session": test_Login.test_login(self, 'pre_online')}
            )
            json_dict_query = json.loads(query.text)
            write_xls(i + 1, 5, float(json_dict_query['data']['total']), file_path)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2,warnings='ignore')