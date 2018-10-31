# -*- coding: utf-8 -*-
# @Time    : 10:46
# @Author  : Administor
# @File    : test_netLoanRegUser.py
# @Software: PyCharm
import unittest
import requests
from config.readConfig import read_config
from common.common import *
import json
from statistics_case.test_Login import test_Login
import time

class test_netLoanRegUser(unittest.TestCase):
    @classmethod
    def setUp(self):
        pass

    s = requests.session()
    def test_net_loan_reg_user(self):
        url = "https://jr.huanqiu.com/set-cookie/?key=version-grey&val=pre"
        l = self.s.get(url)
        register_statis = read_config().get_string('pre_online','register_statis')
        users_statistics = read_config().get_string('pre_online','users_statistics')
        platform_statistics = read_config().get_string('pre_h5','platform_statistics')
        file_name = '当日网贷注册用户数'
        file_path = '..\\testStatistics\\' + file_name + '.xls'
        copy_file(file_name)
        write_xls_time('2018-08-15',file_path)
        xls_list = get_xls(file_path)
        for i in range(1,len(xls_list)):
            start_time = xls_list[i]['开始时间']
            end_time = xls_list[i]['结束时间']
            param_time = time.strftime('%Y-%m-%d', time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
            p = self.s.get(
                platform_statistics + str(param_time),
                json={"Content-Type": "application/json;charset=UTF-8", "huanqiu_backend_session": test_Login.test_login(self,'pre_h5')}
            )
            json_dict_p = json.loads(p.text)
            write_xls(i + 1, 2, float(json_dict_p['data']['sum_name_now']), file_path)

            r = self.s.get(
                register_statis + '&start_time=' + str(param_time) + '&end_time=' + str(param_time),
                json = {"Content-Type": "application/json;charset=UTF-8", "session": test_Login.test_login(self,'pre_online')}
            )
            json_dict = json.loads(r.text)

            for j in json_dict['data']['list']:
                '''
                 @Description:pc返回注册成功人数
                '''
                write_xls(i + 1, 3, float(j['success_regist_people']), file_path)

            m = self.s.get(
                users_statistics + str(param_time) + '|' + str(param_time),
                json={"Content-Type": "application/json;charset=UTF-8","session": test_Login.test_login(self, 'pre_online')}
            )
            json_dict_m = json.loads(m.text)
            for k in json_dict_m['data']['用户情况']:
                '''
                 @Description:pc返回当日注册人数
                '''
                write_xls(i + 1, 4, float(k['mobile']), file_path)
            '''
             @Description:数据库当日网贷注册用户数
            '''
            curr_day_user_sql = "SELECT COUNT(DISTINCT mobile) from users where create_at BETWEEN '" + str(start_time) + "' AND '" + str(end_time) + "'"
            curr_day_user = db_result(curr_day_user_sql)
            write_xls(i + 1, 5, float(curr_day_user[0][0]), file_path)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2,warnings='ignore')