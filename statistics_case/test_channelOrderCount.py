# -*- coding: utf-8 -*-
# @Time    : 14:42
# @Author  : Administor
# @File    : test_channelOrderCount.py
# @Software: PyCharm

import unittest
from config.readConfig import read_config
from common.common import *
import json
import requests
from statistics_case.test_Login import test_Login

class test_channelOrderCount(unittest.TestCase):
    @classmethod
    def setUp(self):
        pass

    s = requests.session()

    '''
     @Description:通过接口得到的数据以及数据库查询结果得到的数据写入excel中，为了方便对比，将返回的结果转换成float类型，直接可以在excel中操作。
                  由于目前sql语句固定，所以暂时将sql语句放在测试脚本中
    '''
    def test_channel_order_count(self):
        url = "https://jr.huanqiu.com/set-cookie/?key=version-grey&val=pre"
        l = self.s.get(url)
        url = read_config().get_string('pre_online','channel_statistics')
        file_name = '渠道订单合计'
        file_path = '..\\testStatistics\\' + file_name + '.xls'
        copy_file(file_name)
        write_xls_time('2018-10-30',file_path)
        xls_list = get_xls(file_path)
        for i in range(1, len(xls_list)):
            start_time = xls_list[i]['开始时间']
            end_time = xls_list[i]['结束时间']
            r = self.s.get(
                url + str(start_time) + '|' + str(end_time),
                json = {"Content-Type": "application/json;charset=UTF-8", "session": test_Login.test_login(self,'pre_online')}
            )
            json_dict = json.loads(r.text)
            account = json_dict['data']['订单渠道'][len(json_dict['data']['订单渠道']) - 1]
            if account['amount'] == '--':
                write_xls(i + 1, 2, float(0), file_path)
            else:
                write_xls(i + 1, 2, float(account['amount']), file_path)

            if account['order_no'] == '--':
                write_xls(i + 1, 3, float(0), file_path)
            else:
                write_xls(i + 1, 3, float(account['order_no']), file_path)

            amount_sql = "select sum(amount) from orders where create_at BETWEEN '" + start_time + "' AND '" + end_time + "' and status in ('HOLDING','DONE')"
            order_sql = "select COUNT(DISTINCT order_no) from orders where create_at BETWEEN '" + start_time + "' AND '" + end_time + "' and status in ('HOLDING','DONE')"
            if db_result(amount_sql) == ((None,),):
                write_xls(i + 1, 4, float(0), file_path)
            else:
                write_xls(i + 1, 4, float(db_result(amount_sql)[0][0]), file_path)
            write_xls(i + 1, 5, float(db_result(order_sql)[0][0]), file_path)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2,warnings='ignore')