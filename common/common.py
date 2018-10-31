# -*- coding: utf-8 -*-
# @Time    : 10:52
# @Author  : Administor
# @File    : common.py
# @Software: PyCharm

from xlrd import open_workbook
from xlutils.copy import copy
import pymysql
import calendar
from shutil import copyfile
import os
import shutil

'''
 @Description:从模板文件夹下拷贝模板文件，并保存在固定位置
'''
def copy_file(file_name):
    file1 = '..\\Template\\' + file_name + '模板.xls'
    file2 = '..\\testStatistics\\' + file_name + '.xls'
    copyfile(file1,file2)

'''
 @Description:根据传入的file_name，行数以及要输入的内容对excel进行修改。注：列暂时写死，适合固定模板
'''
def modify_excel(file_name,num,result_desc):
    wb = open_workbook(file_name)
    wb2 = copy(wb)
    sheet = wb2.get_sheet(0)
    for i in range(num,num + 1):
        sheet.write(i,5,result_desc)
    wb2.save(file_name)
    return

'''
 @Description:获取excel中所有数据，固定格式
'''
def get_excel_all(file_name):
    wb = open_workbook(file_name)
    sheet = wb.sheet_by_name(wb.sheet_names()[0])
    nrows = sheet.nrows
    titleList = sheet.row_values(0)
    cls = []
    for i in range(1,nrows):
        rowValues = sheet.row_values(i)
        caseDict = dict(zip(titleList,rowValues))
        cls.append(caseDict)
    return cls

'''
 @Description:获取excel中所有的内容,注：只针对数据统计
'''
def get_xls(file_name):
    wb = open_workbook(file_name)
    sheet = wb.sheet_by_name(wb.sheet_names()[0])
    nrows = sheet.nrows
    titleList = sheet.row_values(1)
    cls = []
    for i in range(1,nrows):
        rowValues = sheet.row_values(i)
        caseDict = dict(zip(titleList,rowValues))
        cls.append(caseDict)
    return cls

'''
 @Description:将模板拷贝到固定文件夹下，在脚本中输入要查询统计的年、月，将输入的年月所有天数写入excel中
'''
def write_time(year,month,file_name):
    rb = open_workbook(file_name)
    rs = rb.sheet_by_index(0)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    for i in range(calendar.monthrange(year,month)[1]):
        if i + 1 < 10:
            ws.write(i+2,0, str(year) + '-' + str(month) + '-0' + str(i + 1) + ' 00:00:00')
            ws.write(i + 2, 1, str(year) + '-' + str(month) + '-0' + str(i + 1) + ' 23:59:59')
        else:
            ws.write(i + 2, 0, str(year) + '-' + str(month) + '-' + str(i + 1) + ' 00:00:00')
            ws.write(i + 2, 1, str(year) + '-' + str(month) + '-' + str(i + 1) + ' 23:59:59')
    wb.save(file_name)

'''
 @Description:批量生成日期时间，某天开始到当天，代码中的datestart时间是默认的，时间可以随意写，但不能输入当天以后的时间，否则date_list返回[]。
'''
def write_time1(datestart=None,dateend=None):
    import datetime
    if datestart is None:
        datestart = '2018-07-25'
    if dateend is None:
        dateend = datetime.datetime.now().strftime('%Y-%m-%d')

    datestart = datetime.datetime.strptime(datestart,'%Y-%m-%d')
    dateend = datetime.datetime.strptime(dateend,'%Y-%m-%d')
    date_list = []
    date_list.append(datestart.strftime('%Y-%m-%d'))
    while datestart < dateend:
        datestart += datetime.timedelta(days=+1)
        date_list.append(datestart.strftime('%Y-%m-%d'))
    return date_list

'''
 @Description:写入excel中，传入开始时间，文件名，写入某天的00:00:00和23:59:59
'''
def write_xls_time(start_time,file_name):
    rb = open_workbook(file_name)
    rs = rb.sheet_by_index(0)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    time_list = write_time1(start_time)
    for i in range(0,len(time_list)):
        ws.write(i + 2, 0, str(time_list[i]) + ' 00:00:00')
        ws.write(i + 2, 1, str(time_list[i]) + ' 23:59:59')
    wb.save(file_name)

'''
 @Description:将接口以及数据库的返回结果写入excel中
'''
def write_xls(row,col,data,file_name):
    rb = open_workbook(file_name)
    rs = rb.sheet_by_index(0)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    ws.write(row,col,data)
    wb.save(file_name)

'''
 @Description:获取灰度环境对应数据库中的结果
'''
def db_result(sql):
    try:
        connect = pymysql.Connect(host="192.168.1.11", port = 33060, user = "financial_test", passwd = "K948iOskvR!", db = "financial_huanqiu", charset='utf8')
        cursor = connect.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as ex:
        print(str(ex))
    finally:
        cursor.close()
        connect.close()


'''
 @Description:获取测试环境对应数据库中的结果
'''
# def db_result_test(sql):
#     try:
#         connect = pymysql.Connect(host="192.168.1.11", port = 3306, user = "test", passwd = "test@2018", db = "financial_huanqiu", charset='utf8')
#         cursor = connect.cursor()
#         cursor.execute(sql)
#         result = cursor.fetchall()
#         return result
#     except Exception as ex:
#         print(str(ex))
#     finally:
#         cursor.close()
#         connect.close()


'''
 @Description:清空log日志文件
              注：需要将文件定位到position 0，不加这句，文件默认定位到最后，truncate也是从文件最后开始删除
'''
def clear_log(file_name):
    with open(file_name,'r+') as f:
        f.seek(0)
        f.truncate()

'''
 @Description:传入文件夹的相对路径或者绝对路径，删除并新建文件夹
'''
def empty_create_folders(path_name):
    shutil.rmtree(path_name)
    os.makedirs(path_name)
