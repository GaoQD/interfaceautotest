# -*- coding: utf-8 -*-
# @Time    : 16:58
# @Author  : Administor
# @File    : test_Statistics.py
# @Software: PyCharm
import unittest
from common.common import *
from statistics_case.test_Login import test_Login
import json
import requests
import time
from config.readConfig import read_config
import datetime

class test_Statistics(unittest.TestCase):
    @classmethod
    def setUp(self):
        pass

    s = requests.session()
    '''
     @Description:站岗资金统计，由于sql中需要的时间是当前一天以及后一天的时间，因此在代码中添加的部分转换时间的脚本
    '''
    def test_statistics(self):
        url = "https://jr.huanqiu.com/set-cookie/?key=version-grey&val=pre"
        l = self.s.get(url)
        statistics = read_config().get_string('pre_online','statistics')
        json_data = {"Content-Type": "application/json;charset=UTF-8", "session": test_Login.test_login(self,'pre_online')}
        file_name = '站岗资金'
        copy_file(file_name)
        file_path = '..\\testStatistics\\' + file_name + '.xls'
        write_xls_time('2018-07-15',file_path)
        xls_list = get_xls(file_path)
        for i in range(1,len(xls_list)):
            start_time = xls_list[i]['开始时间']
            param_time = time.strftime('%Y-%m-%d', time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
            '''
             @Description:转换时间节点，sql中需要下一天的时间，当前时间加1天
            '''
            end_time = datetime.datetime.strptime(param_time,'%Y-%m-%d') + datetime.timedelta(days=1)
            r = self.s.get(
                statistics + str(param_time) + '|' + str(param_time),
                json=json_data
            )
            json_dict = json.loads(r.text)
            balance = json_dict['data']['站岗资金情况']['balance']
            for j in balance:
                write_xls(i + 1, 2, float(j['amount']), file_path)
                write_xls(i + 1, 3, float(j['users']), file_path)
            amount_sql = "SELECT SUM(o.amount),COUNT(DISTINCT member_id) FROM  (SELECT member_id, SUM(amount) AS amount FROM transaction_record WHERE deal_status = '2' AND  create_time >= '" + str(start_time) + " ' AND create_time < '" + str(end_time.strftime('%Y-%m-%d')) + "'  GROUP BY  member_id) o WHERE o.amount > 0"
            amount = db_result(amount_sql)[0][0]
            if amount == None:
                write_xls(i + 1, 4, float(0), file_path)
            else:
                write_xls(i + 1, 4, float(amount), file_path)
            users = db_result(amount_sql)[0][1]
            write_xls(i + 1, 5, float(users), file_path)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2,warnings='ignore')