# -*- coding: utf-8 -*-
# @Time    : 15:33
# @Author  : Administor
# @File    : test_reimbursementStatistics.py
# @Software: PyCharm
import unittest
from common.common import *
from config.readConfig import read_config
from statistics_case.test_Login import test_Login
import json
import requests

class test_reimbursementStatistics(unittest.TestCase):
    @classmethod
    def setUp(self):
        pass

    s = requests.session()

    '''
     @Description:通过接口得到的数据以及数据库查询结果得到的数据写入excel中，为了方便对比，将返回的结果转换成float类型，直接可以在excel中操作。
    '''
    def test_reimbursement_statistics(self):
        url = "https://jr.huanqiu.com/set-cookie/?key=version-grey&val=pre"
        l = self.s.get(url)
        json_data = {"Content-Type": "application/json;charset=UTF-8", "session": test_Login.test_login(self,'pre_online')}
        return_money_statistics = read_config().get_string('pre_online','return_money_statistics')
        file_name = '回款统计1'
        file_path = '..\\testStatistics\\' + file_name + '.xls'
        copy_file(file_name)
        write_xls_time('2018-07-25',file_path)
        xls_list = get_xls(file_path)

        for i in range(1, len(xls_list)):
            start_time = xls_list[i]['开始时间']
            end_time = xls_list[i]['结束时间']
            user_sql = "SELECT COUNT(DISTINCT member_id) FROM orders WHERE end_time BETWEEN '" + start_time + "' AND '" + end_time + "'"
            total_sql = "SELECT sum(amount+outputmonery) FROM orders WHERE end_time BETWEEN '" + start_time + "' AND '" + end_time + "' AND `status` = 'DONE'"
            forty_sql = "SELECT sum(amount+outputmonery) FROM orders WHERE end_time BETWEEN '" + start_time + "' AND '" + end_time + "' AND time_long=45 AND `status` = 'DONE'"
            forty_user_sql = "SELECT COUNT(DISTINCT member_id) FROM orders WHERE end_time BETWEEN '" + start_time + "' AND '" + end_time + "' AND time_long=45 AND `status` = 'DONE'"
            ninety_sql = "SELECT sum(amount+outputmonery) FROM orders WHERE end_time BETWEEN '" + start_time + "' AND '" + end_time + "' AND time_long=90 AND `status` = 'DONE'"
            ninety_user_sql = "SELECT COUNT(DISTINCT member_id) FROM orders WHERE end_time BETWEEN '" + start_time + "' AND '" + end_time + "' AND time_long=90 AND `status` = 'DONE'"
            one_sql = "SELECT sum(amount+outputmonery) FROM orders WHERE end_time BETWEEN '" + start_time + "' AND '" + end_time + "' AND time_long=180 AND `status` = 'DONE'"
            one_user_sql = "SELECT COUNT(DISTINCT member_id) FROM orders WHERE end_time BETWEEN '" + start_time + "' AND '" + end_time + "' AND time_long=180 AND `status` = 'DONE'"
            three_sql = "SELECT sum(amount+outputmonery) FROM orders WHERE end_time BETWEEN '" + start_time + "' AND '" + end_time + "' AND time_long=365 AND `status` = 'DONE'"
            three_user_sql = "SELECT COUNT(DISTINCT member_id) FROM orders WHERE end_time BETWEEN '" + start_time + "' AND '" + end_time + "' AND time_long=365 AND `status` = 'DONE'"
            user = db_result(user_sql)
            total = db_result(total_sql)
            forty = db_result(forty_sql)
            forty_user = db_result(forty_user_sql)
            ninety = db_result(ninety_sql)
            ninety_user = db_result(ninety_user_sql)
            one = db_result(one_sql)
            one_user = db_result(one_user_sql)
            three = db_result(three_sql)
            three_user = db_result(three_user_sql)

            r = self.s.get(
                return_money_statistics + str(start_time) + '|' + str(end_time),
                json = json_data
            )
            json_dict = json.loads(r.text)
            return_money_list = json_dict['data']['回款情况'].get('return_money')
            for j in range(len(return_money_list)):
                write_xls(i + 1, 2, float(return_money_list[j]['user']), file_path)
                write_xls(i + 1, 4, float(return_money_list[j]['total']), file_path)
                write_xls(i + 1, 6, float(return_money_list[j]['forty_five']), file_path)
                write_xls(i + 1, 7, float(return_money_list[j]['forty_five_user']), file_path)
                write_xls(i + 1, 10, float(return_money_list[j]['ninety']), file_path)
                write_xls(i + 1, 11, float(return_money_list[j]['ninety_user']), file_path)
                write_xls(i + 1, 14, float(return_money_list[j]['one_hundred_and_eighty']), file_path)
                write_xls(i + 1, 15, float(return_money_list[j]['one_hundred_and_eighty_user']), file_path)
                write_xls(i + 1, 18, float(return_money_list[j]['three_hundred_and_sixty']), file_path)
                write_xls(i + 1, 19, float(return_money_list[j]['three_hundred_and_sixty_user']), file_path)

            write_xls(i + 1, 3, float(user[0][0]), file_path)
            if total == ((None,),):
                write_xls(i + 1, 5, float(0), file_path)
            else:
                write_xls(i + 1, 5, float(total[0][0]), file_path)
            write_xls(i + 1, 9, float(forty_user[0][0]), file_path)
            if forty == ((None,),):
                write_xls(i + 1, 8, float(0), file_path)
            else:
                write_xls(i + 1, 8, float(forty[0][0]), file_path)
            if ninety == ((None,),):
                write_xls(i + 1, 12, float(0), file_path)
            else:
                write_xls(i + 1, 12, float(ninety[0][0]), file_path)
            write_xls(i + 1, 13, float(ninety_user[0][0]), file_path)
            if one == ((None,),):
                write_xls(i + 1, 16, float(0), file_path)
            else:
                write_xls(i + 1, 16, float(one[0][0]), file_path)
            write_xls(i + 1, 17, float(one_user[0][0]), file_path)
            if three == ((None,),):
                write_xls(i + 1, 20, float(0), file_path)
            else:
                write_xls(i + 1, 20, float(three[0][0]), file_path)
            write_xls(i + 1, 21, float(three_user[0][0]), file_path)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2,warnings='ignore')