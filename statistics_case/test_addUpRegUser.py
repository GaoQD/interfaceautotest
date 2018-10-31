# -*- coding: utf-8 -*-
# @Time    : 14:39
# @Author  : Administor
# @File    : test_addUpRegUser.py
# @Software: PyCharm
import unittest
from common.common import *
from statistics_case.test_Login import test_Login
import json
import requests
from config.readConfig import read_config
import time

class test_addUpRegUser(unittest.TestCase):
    @classmethod
    def setUp(self):
        pass

    s = requests.session()
    '''
     @Description:累计注册用户数
    '''
    def test_add_up_reg_user(self):
        url = "https://jr.huanqiu.com/set-cookie/?key=version-grey&val=pre"
        l = self.s.get(url)
        platform_statistics = read_config().get_string('pre_h5','platform_statistics')
        register_statis = read_config().get_string('pre_online','register_statis')
        users_statistics = read_config().get_string('pre_online','users_statistics')
        file_name = '累计注册用户数'
        file_path = '..\\testStatistics\\' + file_name + '.xls'
        copy_file(file_name)
        write_xls_time('2018-08-15',file_path)
        xls_list = get_xls(file_path)
        for i in range(1,len(xls_list)):
            start_time = xls_list[i]['开始时间']
            end_time = xls_list[i]['结束时间']
            param_time = time.strftime('%Y-%m-%d',time.strptime(start_time,'%Y-%m-%d %H:%M:%S'))
            r = self.s.get(
                platform_statistics + str(param_time),
                json={"Content-Type": "application/json;charset=UTF-8", "huanqiu_backend_session": test_Login.test_login(self,'pre_h5')}
            )
            json_dict_r = json.loads(r.text)
            '''
             @Description:H5累计注册用户数
            '''
            sum_zhuce_num = json_dict_r['data']['sum_zhuce_num']
            write_xls(i + 1, 2, float(sum_zhuce_num), file_path)
            '''
             @Description:后台注册统计-注册成功人数
            '''
            register = self.s.get(
                str(register_statis) + '&start_time=' + str(param_time) + '&end_time=' + str(param_time),
                json={"Content-Type": "application/json;charset=UTF-8", "huanqiu_backend_session": test_Login.test_login(self,'pre_online')}
            )
            json_dict_register = json.loads(register.text)
            for j in json_dict_register['data']['list']:
                write_xls(i + 1, 3, float(j['success_regist_people']), file_path)
            '''
             @Description:后台 用户统计-注册人数
            '''
            user = self.s.get(
                str(users_statistics) + str(start_time) + '|' + str(end_time),
                json={"Content-Type": "application/json;charset=UTF-8", "session": test_Login.test_login(self,'pre_online')}
            )
            json_dict_user = json.loads(user.text)
            for k in json_dict_user['data']['用户情况']:
                write_xls(i + 1, 4, float(k['mobile']), file_path)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2,warnings='ignore')