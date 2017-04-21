# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import pandas as pd
import xlrd
import re
import pdb
import json

def load_sta_data(filename):
    std_data_path = '{}{}'.format(os.path.dirname(os.path.abspath(__file__)), filename)
    sta = pd.read_csv(std_data_path)
    sta_tables = sta.as_matrix()
    return sta_tables
    
def load_excel(filename, byindex=0):
    test_data = xlrd.open_workbook(filename)
    sheet = test_data.sheets()[byindex]
    return sheet
    
def cell_clear(cell):
    cell = cell.split("（")[0]
    cell = cell.split("(")[0]
    cell = cell.replace('t','').replace(",","").replace(" ","").replace("“","").replace("<","").replace("，","").replace("1",'')
    return cell
    
def extra_info(filename):
    peopleinfo = pd.read_excel(filename)
    tables = peopleinfo.as_matrix()
    
    age = ""
    sexy = ""
    check_time = ""
    report_time = ""
    name = ""
    hospital = ""
    for i in tables:
        for j in i:
            
            check_timepat = '(?:采.*?时间|检验日期|本采集时间|采样时间|核收时间).*?(\d{2,4}.*?\d{1,2}.*?\d{1,2})'.decode("utf8")
            sexypat = '男|女'.decode("utf8")
            agepat = '.*\d{1,}岁|年 龄.*\d{1,}|年齡.*\d{1,}|年龄.*\d{1,}|.*[男|女]\d{1,}'.decode("utf8")
            report_timepat = '报.*?[时间|日期].*?(\d{2,4}.*?\d{1,2}.*?\d{1,2})'.decode("utf8")
            namepat = '姓名.([\\u4e00-\\u9fa5]{2,4})'.decode("utf8")
            hospitalpat = '(.*医院)'.decode("utf8")
            try:
                if re.search(agepat,j):
                    age = re.search(agepat,j).group(0)
                    age=re.compile('\d{1,}').search(age).group(0)
            except:
                continue
                
            try:
                if re.search(sexypat,j):
                    sexy = re.search(sexypat,j).group(0)
            except:
                continue
            
            try:
                if re.search(check_timepat,j):
                    check_time = re.search(check_timepat,j).group(1)
            except:
                continue
                
            try:
                if re.search(report_timepat,j):
                    report_time = re.search(report_timepat,j).group(1)
            except:
                continue

            try:
                if re.search(namepat,j):
                    name = re.search(namepat,j).group(1)
            except:
                continue

            try:
                if re.search(hospitalpat,j):
                    hospital = re.search(hospitalpat,j).group(0)
            except:
                continue
    dict_word={u'姓名':name,u'性别':sexy,u'年龄':age,u'检验日期':check_time,u'报告日期':report_time,u'医院名称':hospital}
    return dict_word

def data_clear(filename, sheetindex=0, stafilename='/stadata/initdata_1373_all.csv'):
    data = load_excel(filename,sheetindex)
    tables = load_sta_data(stafilename)
    matched_cell = []
    unmatched_cell = []
    matched_dic = []
    chinesepat = '[\u4e00-\u9fa5]'.decode('utf-8')
    for rowindex in range(data.nrows):
        for colindex in range(data.ncols):
            cell = data.row_values(rowindex)[colindex].encode('utf-8')
            cell = cell_clear(cell)
            for index in range(len(tables)):
                if cell == tables[index][0]:
                    if cell not in matched_cell:
                        matched_cell.append(cell)
                        dic = {}
                        dic[cell] = data.row_values(rowindex)[colindex+1]
                        matched_dic.append(dic)
                        break
            for index in range(len(tables)):
                if cell not in matched_cell:
                    if not re.search(chinesepat, cell):
                        if cell not in unmatched_cell:
                            unmatched_cell.append(cell)
                            break
            
    info = extra_info(filename)
    #print json.dumps(matched_dic, ensure_ascii=False,indent=4)
    #print json.dumps(info, ensure_ascii=False, indent=4)
    #print json.dumps(unmatched_cell, ensure_ascii=False, indent =4)
    return_dict = {"indicators":matched_dic, "extra_info":info, "unknown_indicators":unmatched_cell}
    #print json.dumps(return_dict, ensure_ascii=False, indent=4)
    return return_dict
    
if __name__ == '__main__':
    data_clear(filename)
