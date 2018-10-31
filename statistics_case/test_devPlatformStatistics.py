# -*- coding: utf-8 -*-
# @Time    : 15:10
# @Author  : Administor
# @File    : test_devPlatformStatistics.py
# @Software: PyCharm
import unittest
import requests
from config.readConfig import read_config
from common.common import *
import json
from statistics_case.test_Login import test_Login
import time

class test_devPlatformStatistics(unittest.TestCase):
    @classmethod
    def setUp(self):
        pass

    s = requests.session()
    '''
     @Description:H5统计数据
    '''
    def test_dev_platform_statistics(self):
        url = "https://jr.huanqiu.com/set-cookie/?key=version-grey&val=pre"
        l = self.s.get(url)
        platform_statistics = read_config().get_string('pre_h5', 'platform_statistics')
        statistics_opr = read_config().get_string('pre_h5', 'statistics_opr')
        file_name = "H5"
        file_path = '..\\testStatistics\\' + file_name + '.xls'
        copy_file(file_name)
        write_xls_time('2018-07-25',file_path)

        xls_list = get_xls(file_path)
        for i in range(1,len(xls_list)):
            start_time = xls_list[i]['开始时间']
            end_time = xls_list[i]['结束时间']
            '''
             @Description:转换时间格式
            '''
            param_time = time.strftime('%Y-%m-%d', time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
            date_time = time.strftime('%Y%m%d', time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
            r = self.s.get(
                platform_statistics + str(param_time),
                json={"Content-Type": "application/json;charset=UTF-8", "huanqiu_backend_session": test_Login.test_login(self,'pre_h5')}
            )
            json_dict = json.loads(r.text)

            t = self.s.get(
                statistics_opr + str(date_time)
            )
            json_dict_t = json.loads(t.text)
            ADD_UP_IN_COME = json_dict_t['OVERVIEW']['ADD_UP_IN_COME']
            ADD_UP_PAY_USER = json_dict_t['OVERVIEW']['ADD_UP_PAY_USER']
            '''
             @Description:累计投资金额
            '''
            write_xls(i + 1, 2, float(json_dict['data']['sum_amount']), file_path)

            '''
             @Description:累计投资金额
            '''
            add_up_ord_amt_sql = "select sum(amount) from orders where status in ('HOLDING','DONE')"
            write_xls(i + 1, 3, float(db_result(add_up_ord_amt_sql)[0][0]), file_path)
            '''
             @Description:玖富累计投资金额
            '''
            write_xls(i + 1, 4, float(json_dict['data']['sum_amount_9f']), file_path)
            '''
             @Description:天天热卖累计交易额
            '''
            write_xls(i + 1, 5, float(json_dict['data']['sum_amount_tiantian']), file_path)
            '''
             @Description:当日交易额
            '''
            write_xls(i + 1, 6, float(json_dict['data']['sum_amount_now']), file_path)
            '''
             @Description:当日交易额
            '''
            curr_day_ord_amt_sql = "SELECT sum(amount) from orders WHERE `status` in ('DONE','HOLDING') and create_at BETWEEN '" + str(start_time) + "' and '" + str(end_time) + "'"
            curr_day_ord_amt = db_result(curr_day_ord_amt_sql)
            if curr_day_ord_amt == ((None,),):
                write_xls(i + 1, 7, float(0), file_path)
            else:
                write_xls(i + 1, 7, float(db_result(curr_day_ord_amt_sql)[0][0]), file_path)
            '''
             @Description:玖富当日交易额
            '''
            write_xls(i + 1, 8, float(json_dict['data']['sum_amount_now_9f']), file_path)
            '''
             @Description:天天热卖当日交易额
            '''
            write_xls(i + 1, 9, float(json_dict['data']['sum_amount_now_tiantian']), file_path)
            '''
             @Description:累计投资用户数
            '''
            write_xls(i + 1, 10, float(json_dict['data']['sum_name']), file_path)
            '''
             @Description:累计投资用户数
            '''
            add_up_pay_user_sql = "select count(distinct mobile) from orders where status in ('HOLDING','DONE')"
            write_xls(i + 1, 11, float(db_result(add_up_pay_user_sql)[0][0]), file_path)
            '''
             @Description:天天热卖累计投资用户数
            '''
            write_xls(i + 1, 12, float(ADD_UP_PAY_USER), file_path)
            '''
             @Description:当日投资用户数
            '''
            write_xls(i + 1, 13, float(json_dict['data']['sum_name_now']), file_path)

            '''
             @Description:当日投资用户数
            '''
            curr_day_pay_user_sql = "SELECT COUNT(DISTINCT member_id) from orders WHERE `status` in ('DONE','HOLDING') and create_at BETWEEN '" + str(start_time) + "' and  '" + str(end_time) + "'"
            write_xls(i + 1, 14, float(db_result(curr_day_pay_user_sql)[0][0]), file_path)
            '''
             @Description:天天热卖累计交易额
            '''
            # write_xls(i +1, 5,float(json_dict['data']['sum_amount_tiantian']), file_path)


            '''
             @Description:当前存量金额
            '''
            write_xls(i + 1, 15, float(json_dict['data']['sum_stock_amount']), file_path)
            '''
             @Description:玖富当前存量金额
            '''
            write_xls(i + 1, 16, float(json_dict['data']['sum_stock_amount_9f']), file_path)
            '''
             @Description:天天热卖当前存量金额
            '''
            write_xls(i + 1, 17, float(json_dict['data']['sum_stock_num_now_tiantian']), file_path)
            '''
             @Description:当前存量金额
            '''
            stock_ord_smt_sql = "select case when SUM(amount) is null then 0 else SUM(amount) end as amount from orders  where status ='HOLDING' and create_at <= '" + str(end_time) + "'"
            reimbursement_sql = "select case when sum(amount) is null then 0 else sum(amount) end as amount from transaction_record where deal_status=2 and create_time <= '" + str(end_time) + "' and trade_type=5"

            write_xls(i + 1, 18, float(db_result(stock_ord_smt_sql)[0][0]) - float(db_result(reimbursement_sql)[0][0]), file_path)
            '''
             @Description:累计注册用户数
            '''
            write_xls(i + 1, 19, float(json_dict['data']['sum_zhuce_num']), file_path)
            '''
             @Description:累计注册用户数
            '''
            add_up_reg_user_sql = "SELECT COUNT(DISTINCT mobile) FROM users"
            write_xls(i + 1, 20, float(db_result(add_up_reg_user_sql)[0][0]), file_path)


            write_xls(i + 1, 21, float(json_dict['data']['sum_zhuce_num_now']), file_path)
            write_xls(i + 1, 22, float(json_dict['data']['sum_zhuce_num_now_9f']), file_path)
            '''
             @Description:当前存量用户数
            '''
            write_xls(i + 1, 23, float(json_dict['data']['user_holding']), file_path)
            '''
             @Description:当前存量用户数
            '''
            curr_day_stock_ord_user_sql = "SELECT COUNT(DISTINCT member_id) from orders WHERE `status` in ('HOLDING')"
            write_xls(i + 1, 24, float(db_result(curr_day_stock_ord_user_sql)[0][0]), file_path)
            '''
             @Description:为客户赚取收益
            '''
            write_xls(i + 1, 25, float(json_dict['data']['user_rate_amount']), file_path)

            '''
             @Description:为用户赚取收益
            '''
            add_up_in_come_sql = "select SUM(outputmonery) from orders where status in ('HOLDING','DONE') and create_at <= '" + str(end_time) + "'"
            write_xls(i + 1, 26, float(db_result(add_up_in_come_sql)[0][0]) + float(ADD_UP_IN_COME), file_path)
            '''
             @Description:当日网贷注册用户数
            '''
            curr_day_user_sql = "SELECT COUNT(DISTINCT mobile) from users where create_at BETWEEN '" + str(start_time) + "' AND  '" + str(end_time) + "'"
            # write_xls(i + 1, 18, float(db_result(curr_day_user_sql)[0][0]), file_path)
            '''
             @Description:当日网贷投资金额
            '''
            curr_day_total_sql = "SELECT sum(amount) from orders WHERE `status` in ('DONE','HOLDING') and create_at BETWEEN '" + str(start_time) + "' and '" + str(end_time) + "'"
            curr_day_total = db_result(curr_day_total_sql)
            # if curr_day_total == ((None,),):
            #     write_xls(i + 1, 19, float(0), file_path)
            # else:
            #     write_xls(i + 1, 19, float(curr_day_total[0][0]), file_path)


            '''
             @Description:累计交易额
            '''
            add_up_ord_sql = "select sum(amount) from orders where status in ('HOLDING','DONE')"
            # write_xls(i + 1, 28, float(db_result(add_up_ord_sql)[0][0]), file_path)

    def  tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2,warnings='ignore')