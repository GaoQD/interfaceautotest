# -*- coding: utf-8 -*-
# @Time    : 13:47
# @Author  : Administor
# @File    : test_orderCount.py
# @Software: PyCharm

import unittest
import requests
from config.readConfig import read_config
from common.common import *
import json
from statistics_case.test_Login import test_Login

class test_orderCount(unittest.TestCase):
    @classmethod
    def setUp(self):
        pass

    s = requests.session()
    '''
     @Description:通过接口得到的数据以及数据库查询结果得到的数据写入excel中，为了方便对比，将返回的结果转换成float类型，直接可以在excel中操作
    '''
    def test_order_count(self):
        url = "https://jr.huanqiu.com/set-cookie/?key=version-grey&val=pre"
        l = self.s.get(url)
        order_count = read_config().get_string('pre_online','order_count')
        json_data = {"Content-Type": "application/json;charset=UTF-8", "session":test_Login.test_login(self,'pre_online')}
        pageNO = 1
        file_name = '订单合计'
        copy_file(file_name)
        file_path = '..\\testStatistics\\' + file_name + '.xls'
        write_xls_time('2018-07-25',file_path)
        xls_list = get_xls(file_path)
        for i in range(1,len(xls_list)) :
            start_time = xls_list[i]['开始时间']
            end_time = xls_list[i]['结束时间']
            r = self.s.get(
                str(order_count) + str(pageNO) + '&channel=&date=' + str(start_time) + '|' + str(end_time),
                json = json_data
            )
            json_dict = json.loads(r.text)
            if json_dict['data']['total'] > 10 :
                r = self.s.get(
                    str(order_count) + str(pageNO + int(json_dict['data']['total']/11)) + '&channel=&date=' + str(start_time) + '|' + str(end_time),
                    json = json_data
                )
                json_dict1 = json.loads(r.text)
                account1 = json_dict1['data']['data'][len(json_dict1['data']['data']) - 1]

                if account1['amount'] == '--':
                    write_xls(i + 1, 2, float(0), file_path)
                else:
                    write_xls(i + 1, 2, float(account1['amount']), file_path)
                write_xls(i + 1, 3, float(account1['order_sum']), file_path)
                write_xls(i + 1, 4, float(account1['people_sum']), file_path)
            else:
                account = json_dict['data']['data'][len(json_dict['data']['data']) - 1]
                if account['amount'] == '--':
                    write_xls(i + 1, 2, float(0), file_path)
                else:
                    write_xls(i + 1, 2, float(account['amount']), file_path)
                write_xls(i + 1, 3, float(account['order_sum']), file_path)
                write_xls(i + 1, 4, float(account['people_sum']), file_path)
            amount_sql = "select sum(amount) from orders where create_at BETWEEN '" + start_time + "' AND '" + end_time + "' and status in ('HOLDING','DONE')"
            order_sql = "SELECT COUNT(order_no) FROM orders where create_at BETWEEN '" + start_time + "' AND '" + end_time + "' and status in ('HOLDING','DONE')"
            member_sql = "select count(DISTINCT member_id) from orders where create_at BETWEEN '" + start_time + "' AND '" + end_time + "' and status in ('HOLDING','DONE')"
            if db_result(amount_sql) == ((None,),):
                write_xls(i + 1, 5, float(0), file_path)
            else:
                write_xls(i + 1, 5, db_result(amount_sql)[0][0], file_path)
            write_xls(i + 1, 6, db_result(order_sql)[0][0], file_path)
            write_xls(i + 1, 7, db_result(member_sql)[0][0], file_path)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2,warnings='ignore')