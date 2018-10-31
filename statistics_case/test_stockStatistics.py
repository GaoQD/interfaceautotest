# -*- coding: utf-8 -*-
# @Time    : 15:02
# @Author  : Administor
# @File    : test_stockStatistics.py
# @Software: PyCharm
import unittest
from common.common import *
from statistics_case.test_Login import test_Login
import json
import requests
from config.readConfig import read_config

class test_stockStatistics(unittest.TestCase):
    @classmethod
    def setUp(self):
        pass

    s =  requests.session()

    '''
     @Description:通过接口得到的数据以及数据库查询结果得到的数据写入excel中，为了方便对比，将返回的结果转换成float类型，直接可以在excel中操作。
    '''
    def test_stock_statistics(self):
        url = "https://jr.huanqiu.com/set-cookie/?key=version-grey&val=pre"
        l = self.s.get(url)
        stock_statistics = read_config().get_string('pre_online','stock_statistics')
        file_name = '存量合计'
        file_path = '..\\testStatistics\\' + file_name + '.xls'
        copy_file(file_name)
        write_xls_time('2018-07-15',file_path)
        xls_list = get_xls(file_path)
        json_data = {"Content-Type": "application/json;charset=UTF-8", "session": test_Login.test_login(self,'pre_online')}
        for i in range(1, len(xls_list)) :
            start_time = xls_list[i]['开始时间']
            end_time = xls_list[i]['结束时间']
            done_sum_sql1 = "SELECT SUM(amount) FROM orders WHERE  create_at >= '" + str(start_time) + "' AND create_at <= '" + str(end_time) + "' AND `status` IN('HOLDING','DONE')"
            done_sum_sql2 = "SELECT SUM(amount) FROM orders WHERE end_time >= '" + str(start_time) + "' AND end_time <= '" + str(end_time) + "' AND `status` IN('HOLDING','DONE')"
            stock_four_sql = "SELECT sum(amount)  from orders where create_at BETWEEN '" + start_time + "' AND '" + end_time + "' and status in ('HOLDING') and time_long = 45"
            stock_ninth_sql = "SELECT sum(amount)  from orders where create_at BETWEEN '" + start_time + "' AND '" + end_time + "' and status in ('HOLDING') and time_long = 90"
            stock_one_sql = "SELECT sum(amount)  from orders where create_at BETWEEN '" + start_time + "' AND '" + end_time + "' and status in ('HOLDING') and time_long = 180"
            stock_three_sql = "SELECT sum(amount)  from orders where create_at BETWEEN '" + start_time + "' AND '" + end_time + "' and status in ('HOLDING') and time_long = 365"

            done_sum1 = db_result(done_sum_sql1)
            done_sum2 = db_result(done_sum_sql2)
            stock_four = db_result(stock_four_sql)
            stock_ninth = db_result(stock_ninth_sql)
            stock_one = db_result(stock_one_sql)
            stock_three = db_result(stock_three_sql)
            r = self.s.get(
                stock_statistics + str(start_time) + '|' + str(end_time),
                json = json_data
            )
            json_dict = json.loads(r.text)
            stock_list = json_dict['data']['存量情况'].get('stock_list')
            for j in range(len(stock_list)):
                write_xls(i + 1, 2, float(stock_list[j]['done_sum']), file_path)
                write_xls(i + 1, 3, float(stock_list[j]['total']), file_path)
                write_xls(i + 1, 4, float(stock_list[j]['stock_four']), file_path)
                write_xls(i + 1, 5, float(stock_list[j]['stock_ninth']), file_path)
                write_xls(i + 1, 6, float(stock_list[j]['stock_one_hundred']), file_path)
                write_xls(i + 1, 7, float(stock_list[j]['stock_three_hundred']), file_path)

            if done_sum1 == ((None,),):
                if done_sum2 == ((None,),):
                    write_xls(i + 1, 8 , float(0), file_path)
                else:
                    write_xls(i + 1, 8, float(done_sum2[0][0]), file_path)
            else:
                if done_sum2 == ((None,),):
                    write_xls(i + 1, 8, float(done_sum1[0][0]), file_path)
                else:
                    write_xls(i + 1, 8, float(done_sum1[0][0]) - float(done_sum2[0][0]), file_path)

            '''
             @Description:当前存量金额
            '''
            stock_ord_smt_sql = "select case when SUM(amount) is null then 0 else SUM(amount) end as amount from orders  where status ='HOLDING' and create_at <= '" + str(end_time) + "'"
            reimbursement_sql = "select case when sum(amount) is null then 0 else sum(amount) end as amount from transaction_record where deal_status=2 and create_time <= '" + str(end_time) + "' and trade_type=5"
            write_xls(i + 1, 9, float(db_result(stock_ord_smt_sql)[0][0]) - float(db_result(reimbursement_sql)[0][0]), file_path)
            if stock_four == ((None,),) :
                write_xls(i + 1, 10, float(0), file_path)
            else:
                write_xls(i + 1, 10, float(stock_four[0][0]), file_path)

            if stock_ninth == ((None,),) :
                write_xls(i + 1, 11, float(0), file_path)
            else:
                write_xls(i + 1, 11, float(stock_ninth[0][0]), file_path)

            if stock_one == ((None,),):
                write_xls(i + 1, 12, float(0), file_path)
            else:
                write_xls(i + 1, 12, float(stock_one[0][0]), file_path)

            if stock_three == ((None,),):
                write_xls(i + 1, 13, float(0), file_path)
            else:
                write_xls(i + 1, 13, float(stock_three[0][0]), file_path)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2,warnings='ignore')