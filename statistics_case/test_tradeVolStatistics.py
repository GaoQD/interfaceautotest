# -*- coding: utf-8 -*-
# @Time    : 9:16
# @Author  : Administor
# @File    : test_tradeVolStatistics.py
# @Software: PyCharm
import unittest
from common.common import *
from statistics_case.test_Login import test_Login
import json
import requests
from config.readConfig import read_config
import time

class test_tradeVolStatistics(unittest.TestCase):
    @classmethod
    def setUp(self):
        pass

    s = requests.session()

    def test_trade_vol_statistics(self):
        url = "https://jr.huanqiu.com/set-cookie/?key=version-grey&val=pre"
        l = self.s.get(url)
        file_name = '当日交易额'
        copy_file(file_name)
        file_path = '..\\testStatistics\\' + file_name + '.xls'
        write_xls_time('2018-07-15',file_path)
        order_count = read_config().get_string('pre_online','order_count')
        channel_order = read_config().get_string('pre_online','channel_statistics')
        users_statistics = read_config().get_string('pre_online','users_statistics')
        platform_statistics = read_config().get_string('pre_h5','platform_statistics')
        pageNO = 1
        xls_list = get_xls(file_path)
        for i in range(1,len(xls_list)):
            start_time = xls_list[i]['开始时间']
            end_time = xls_list[i]['结束时间']
            param_time = time.strftime('%Y-%m-%d',time.strptime(start_time,'%Y-%m-%d %H:%M:%S'))
            r = self.s.get(
                platform_statistics + str(param_time),
                json={"Content-Type":"application/json;charset=UTF-8","huanqiu_backend_session":test_Login.test_login(self,'pre_h5')}
            )
            json_dict = json.loads(r.text)
            '''
             @Description:H5当日交易额
            '''
            sum_amount_now = json_dict['data']['sum_amount_now']
            write_xls(i + 1, 2, float(sum_amount_now), file_path)
            sum_amount_now_9f = json_dict['data']['sum_amount_now_9f']
            write_xls(i + 1, 3, float(sum_amount_now_9f), file_path)

            '''
             @Description:PC 订单统计-当日投资金额
            '''

            order = self.s.get(
                str(order_count) + str(pageNO) + '&channel=&date=' + str(start_time) + '|' + str(end_time),
                json={"Content-Type": "application/json;charset=UTF-8","huanqiu_backend_session": test_Login.test_login(self, 'pre_online')}
            )
            json_dict_order = json.loads(order.text)
            if json_dict_order['data']['total'] > 10:
                ord = self.s.get(
                    str(order_count) + str(pageNO + int(json_dict_order['data']['total']/11)) + '&channel=&date=' + str(start_time) + '|' + str(end_time),
                    json={"Content-Type": "application/json;charset=UTF-8","huanqiu_backend_session": test_Login.test_login(self, 'pre_online')}
                )
                json_dict_ord = json.loads(ord.text)
                account = json_dict_ord['data']['data'][len(json_dict_ord['data']['data']) - 1]
                write_xls(i + 1, 4, float(account['amount']), file_path)
            else:
                amount = json_dict_order['data']['data'][len(json_dict_order['data']['data']) - 1]
                if amount['amount'] == '--':
                    write_xls(i + 1, 4, float(0), file_path)
                else:
                    write_xls(i + 1, 4, float(amount['amount']), file_path)

            '''
             @Description:PC 渠道订单统计-订单金额
            '''
            channel = self.s.get(
                str(channel_order) + str(param_time) + '|' + str(end_time),
                json={"Content-Type":"application/json;charset=UTF-8","session":test_Login.test_login(self,'pre_online')}
            )
            json_dict_channel = json.loads(channel.text)
            if json_dict_channel['data']['total'] == 1:
                write_xls(i + 1, 5, float(0), file_path)
            elif json_dict_channel['data']['total'] > 10:
                chanel = self.s.get(
                    str(channel_order) + str(param_time) + '|' + str(end_time),
                    json={"Content-Type": "application/json;charset=UTF-8","session": test_Login.test_login(self, 'pre_online')}
                )
                json_dict_chanel = json.loads(chanel.text)
                chanel_amount = json_dict_chanel['data']['订单渠道'][len(json_dict_chanel['data']['订单渠道']) - 1]
                write_xls(i + 1, 5, float(chanel_amount['amount']), file_path)
            else:
                channel_sta = self.s.get(
                    str(channel_order) + str(param_time) + '|' + str(end_time),
                    json={"Content-Type": "application/json;charset=UTF-8","session": test_Login.test_login(self, 'pre_online')}
                )
                json_dict_channel_sta = json.loads(channel_sta.text)
                channel_sta_amount = json_dict_channel_sta['data']['订单渠道'][len(json_dict_channel_sta['data']['订单渠道']) - 1]
                write_xls(i + 1, 5, float(channel_sta_amount['amount']), file_path)

            '''
             @Description:PC 资金统计-当日购买总额 
            '''
            user = self.s.get(
                str(users_statistics) + str(param_time) + '|' + str(param_time),
                json={"Content-Type": "application/json;charset=UTF-8","session": test_Login.test_login(self, 'pre_online')}
            )
            json_dict_user = json.loads(user.text)
            account_user = json_dict_user['data']['资金情况'][len(json_dict_user['data']['资金情况']) - 1]
            write_xls(i + 1, 6, float(account_user['total_amount']), file_path)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2,warnings='ignore')