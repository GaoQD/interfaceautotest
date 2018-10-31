# -*- coding: utf-8 -*-
# @Time    : 17:20
# @Author  : Administor
# @File    : test_ALL_Case.py
# @Software: PyCharm
import unittest
import HTMLTestRunner
from common.common import *
from statistics_case.test_Login import test_Login
from statistics_case.test_orderCount import test_orderCount
from common.send_Email import send_email
import time

if __name__ == '__main__':
    clear_log('..\\log\\test.log')
    empty_create_folders('..\\testStatistics')
    suite = unittest.TestSuite
    suite.addTest(test_Login('test_login'))
    suite.addTest(test_orderCount('test_order_count'))
    now_time = time.strftime("%Y%m%M%H%M%S", time.localtime(time.time()))
    # fp = open('..\\testStatistics\\订单合计.xls','wb')
    runner = HTMLTestRunner.HTMLTestRunner(
        # stream=fp,
        title='statistics test',
        verbosity=2,
        description='statistics test run result'
    )
    runner.run(suite)
    send_email(now_time)