# -*- coding: utf-8 -*-
# @Time    : 9:11
# @Author  : Administor
# @File    : test_platformStatistics.py
# @Software: PyCharm

import unittest
import requests
from config.readConfig import read_config
from common.common import *
import json
from statistics_case.test_Login import test_Login
import time

class test_platformStatistics(unittest.TestCase):
    @classmethod
    def setUp(self):
        pass

    s = requests.session()

    def test_platform_statistics(self):
        platform_statistics = read_config().get_string('statistics','platform_statistics')
        json_data = {"Content-Type": "application/json;charset=UTF-8", "session": test_Login.test_login(self)}
        file_name = "H5统计数据"
        file_path = '..\\testStatistics\\' + file_name + '.xls'
        xls_list = get_xls(file_path)
        for i in range(1,len(xls_list)):
            start_time = xls_list[i]['开始时间']
            end_time = xls_list[i]['结束时间']
            date_time = time.strftime('%Y-%m-%d', time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
            r = self.s.get(
                platform_statistics + str(date_time),
                json=json_data
            )
            json_dict = json.loads(r.text)
            '''
             @Description:当日投资用户数
            '''
            sum_name_now = json_dict['data']['sum_name_now']
            write_xls(i + 1, 6, float(sum_name_now), file_path)
            sum_amount = json_dict['data']['sum_amount']
            # print(json_dict['data']['sum_zhuce_num_now_9f'])
            # print(sum_name_now)
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2,warnings='ignore')