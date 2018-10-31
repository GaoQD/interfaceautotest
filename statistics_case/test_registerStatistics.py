# -*- coding: utf-8 -*-
# @Time    : 16:13
# @Author  : Administor
# @File    : test_registerStatistics.py
# @Software: PyCharm
import unittest
from common.common import *
from statistics_case.test_Login import test_Login
import json
import requests
from config.readConfig import read_config
import time

class test_registerStatistics(unittest.TestCase):
    @classmethod
    def setUp(self):
        pass

    s = requests.session()
    '''
     @Description:注册统计失败人数，接口返回，数据库中无法拿到数据---柴伟泰
    '''
    def test_register_statistics(self):
        url = "https://jr.huanqiu.com/set-cookie/?key=version-grey&val=pre"
        l = self.s.get(url)
        register_statis = read_config().get_string('pre_online','register_statis')
        file_name = '注册统计'
        copy_file(file_name)
        file_path = '..\\testStatistics\\' + file_name + '.xls'
        write_xls_time('2018-08-01',file_path)
        xls_list = get_xls(file_path)
        for i in range(1,len(xls_list)):
            start_time = xls_list[i]['开始时间']
            end_time = xls_list[i]['结束时间']
            param_time = time.strftime('%Y-%m-%d', time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
            register_sql = "SELECT COUNT(*) FROM users WHERE create_at BETWEEN '" + str(start_time) +"' AND '" + str(end_time) + "'"
            write_xls(i + 1, 4, float(db_result(register_sql)[0][0]), file_path)
            r = self.s.get(
                str(register_statis) + '&start_time=' + str(param_time) + '&end_time=' + str(param_time),
                json={"Content-Type": "application/json;charset=UTF-8", "session": test_Login.test_login(self,'pre_online')}
            )
            json_dict = json.loads(r.text)
            return_list = json_dict['data']['list']
            for j in return_list:
                write_xls(i + 1, 2, float(j['success_regist_people']), file_path)
                write_xls(i + 1, 3, float(j['fail_regist_people']), file_path)



    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2,warnings='ignore')