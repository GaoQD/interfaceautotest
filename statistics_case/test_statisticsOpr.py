# -*- coding: utf-8 -*-
# @Time    : 9:46
# @Author  : Administor
# @File    : test_statisticsOpr.py
# @Software: PyCharm
import unittest
import requests
from config.readConfig import read_config
from common.common import *
import json
from statistics_case.test_Login import test_Login
from statistics_case.test_platformStatistics import test_platformStatistics
import time

class test_statisticsOpr(unittest.TestCase):
    @classmethod
    def setUp(self):
        pass

    s = requests.session()
    '''
     @Description:天天热卖接口返回
    '''
    def test_statistics_opr(self):
        url = read_config().get_string('statistics','statistics_opr')
        json_data = {"Content-Type": "application/json;charset=UTF-8", "session": test_Login.test_login(self)}
        # year = 2018
        # month = 9
        file_name = "H5"
        # copy_file(file_name)
        file_path = '..\\testStatistics\\' + file_name + '.xls'
        ADD_UP_IN_COME = ''
        # write_time(year,month,file_path)
        xls_list = get_xls(file_path)
        for i in range(1,len(xls_list)):
            start_time = xls_list[i]['开始时间']
            end_time = xls_list[i]['结束时间']
            param_time = time.strftime('%Y%m%d',time.strptime(start_time,'%Y-%m-%d %H:%M:%S'))
            r = self.s.get(
                url + str(param_time),
                json = json_data
            )
            json_dict = json.loads(r.text)
            ADD_UP_IN_COME = json_dict['OVERVIEW']['ADD_UP_IN_COME']
            print(ADD_UP_IN_COME)
        return ADD_UP_IN_COME
            #
            # '''
            #  @Description:当日网贷注册用户数sql语句，只统计环球金融
            # '''
            # curr_day_user_sql = "SELECT COUNT(DISTINCT mobile) from users where create_at BETWEEN '" + str(start_time) + "' AND  '" + str(end_time) + "'"
            # write_xls(i + 1, 2, db_result(curr_day_user_sql)[0][0], file_path)
            #
            # '''
            #  @Description:当日网贷投资金额sql语句，只统计环球金融
            # '''
            # curr_day_total_sql = "SELECT sum(amount) from orders WHERE `status` in ('DONE','HOLDING') and create_at BETWEEN '" + str(start_time) + "' and '" + str(end_time) + "'"
            # curr_day_total = db_result(curr_day_total_sql)
            # if curr_day_total == ((None,),):
            #     write_xls(i + 1, 3, float(0), file_path)
            # else:
            #     write_xls(i + 1, 3, float(curr_day_total[0][0]), file_path)
            # '''
            #  @Description:当日投资用户数
            # '''
            # CURR_DAY_PAY_USER = json_dict['OVERVIEW'].get('CURR_DAY_PAY_USER')
            # curr_day_pay_user_sql = "SELECT COUNT(DISTINCT member_id) from orders WHERE `status` in ('DONE','HOLDING') and create_at BETWEEN '" + str(start_time) + "' and  '" + str(end_time) + "'"
            # write_xls(i + 1, 4, float(db_result(curr_day_pay_user_sql)[0][0]), file_path)
            # write_xls(i + 1, 5, float(CURR_DAY_PAY_USER), file_path)
            #
            # '''
            #  @Description:当前存量用户数
            # '''
            # CURR_DAY_STOCK_ORD_USER = json_dict['OVERVIEW'].get('CURR_DAY_STOCK_ORD_USER')
            # curr_day_stock_ord_user_sql = "SELECT COUNT(DISTINCT member_id) from orders WHERE `status` in ('HOLDING')"
            # write_xls(i + 1, 7, float(CURR_DAY_STOCK_ORD_USER) + float(db_result(curr_day_stock_ord_user_sql)[0][0]), file_path)
            #
            # '''
            #  @Description:累计投资金额
            # '''
            # ADD_UP_ORD_AMT = json_dict['OVERVIEW'].get('ADD_UP_ORD_AMT')
            # add_up_ord_amt_sql = "select sum(amount) from orders where status in ('HOLDING','DONE')"
            # write_xls(i + 1, 8, float(ADD_UP_ORD_AMT) + float(db_result(add_up_ord_amt_sql)[0][0]), file_path)
            #
            # '''
            #  @Description:累计注册用户数，只统计环球金融
            # '''
            # add_up_reg_user_sql = "SELECT COUNT(DISTINCT mobile) FROM users"
            # write_xls(i + 1, 9, db_result(add_up_reg_user_sql)[0][0], file_path)
            #
            # '''
            #  @Description:累计投资用户数
            # '''
            # ADD_UP_PAY_USER = json_dict['OVERVIEW'].get('ADD_UP_PAY_USER')
            # add_up_pay_user_sql = "select count(distinct mobile) from orders where status in ('HOLDING','DONE')"
            # write_xls(i + 1, 10, float(ADD_UP_PAY_USER) + float(db_result(add_up_pay_user_sql)[0][0]), file_path)
            #
            # '''
            #  @Description:当前存量金额
            # '''
            # STOCK_ORD_AMT = json_dict['ALLOCATION'].get('STOCK_ORD_AMT')
            # stock_ord_smt_sql = "SELECT((select case when SUM(amount) is null then 0 else SUM(amount) end as amount from orders  " \
            #                     "where status ='HOLDING' and create_at < '" + str(end_time) + "')-(select case when sum(amount) is " \
            #                                                                                   "null then 0 else sum(amount) end as amount from transaction_record where deal_status=2 and create_time <= '" + str(end_time) + "' and trade_type=5))"
            # write_xls(i + 1, 11, float(STOCK_ORD_AMT) + float(db_result(stock_ord_smt_sql)[0][0]), file_path)
            # '''
            #  @Description:为用户赚取收益
            # '''
            # ADD_UP_IN_COME = json_dict['OVERVIEW'].get('ADD_UP_IN_COME')
            # add_up_in_come_sql = "select SUM(outputmonery) from orders where status in ('HOLDING','DONE') and create_at <= '" + str(end_time) + "'"
            # write_xls(i + 1, 12, float(ADD_UP_IN_COME)  + float(db_result(add_up_in_come_sql)[0][0]), file_path)
            # '''
            #  @Description:当日交易额，只统计环球金融
            # '''
            # curr_day_ord_amt_sql = "SELECT sum(amount) from orders WHERE `status` in ('DONE','HOLDING') and create_at BETWEEN '" + str(start_time) + "' and '" + str(end_time) + "'"
            # curr_day_ord_amt = db_result(curr_day_ord_amt_sql)
            # if curr_day_ord_amt == ((None,),):
            #     write_xls(i +1, 13, float(0), file_path)
            # else:
            #     write_xls(i + 1, 13, float(db_result(curr_day_ord_amt_sql)[0][0]), file_path)
            # '''
            #  @Description:累计交易额
            # '''
            # ADD_UP_ORD_AMT = json_dict['ALLOCATION'].get('ADD_UP_ORD_AMT')
            # add_up_ord_sql = "select sum(amount) from orders where status in ('HOLDING','DONE')"
            # write_xls(i + 1, 14, float(db_result(add_up_ord_sql)[0][0]), file_path)
            # write_xls(i + 1, 15, float(ADD_UP_ORD_AMT), file_path)
            #
            # '''
            #  @Description:当前存量
            # '''
            # CURR_STOCK = json_dict['ALLOCATION'].get('STOCK_ORD_AMT')
            # write_xls(i + 1, 16, float(db_result(stock_ord_smt_sql)[0][0]), file_path)
            # write_xls(i + 1, 17, float(CURR_STOCK), file_path)
            # test_platformStatistics.test_platform_statistics(self)
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2,warnings='ignore')