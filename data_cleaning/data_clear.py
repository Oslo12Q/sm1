# -*- coding: utf-8 -*-
import logging
import os
import pandas as pd
import xlrd
import re

std_data_path = '{}{}'.format(os.path.dirname(os.path.abspath(__file__)), '/stadata/initdata_1373_all.csv')
sta = pd.read_csv(std_data_path)
tables = sta.as_matrix()


def data_clear(filename):
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]

    a = []
    for i in range(table.nrows):
        for j in range(len(table.row_values(i))-1):
            m0=table.row_values(i-1)[j].encode('utf-8')
            m1=table.row_values(i)[j].encode('utf-8')
            m1=m1.split("（")[0]
            m1=m1.split("(")[0]
            m2=table.row_values(i)[j+1]
            for k in range(len(tables)):
                if (m1 == tables[k][0] or m1 == tables[k][1] or m0 == tables[k][1])and len(m1)>2:
                    #print m1,m2
                    try:
                        d={}
                        d["key"]=m1
                        d["value"]=float(m2.encode('utf-8').replace('t','').replace(",","").replace(" ","").replace("“","").replace("<",""))
                        a.append(d)
                    except:
                        continue
    aa=[]
    for i in a:
        if i not in aa:
            aa.append(i)
    
    peopledata=pd.read_excel(filename)
    mdata=peopledata.as_matrix()
    
    age = "".decode("utf-8")
    sexy = "".decode("utf-8")
    check_time = "".decode("utf-8")
    report_time = "".decode("utf-8")
    name = "".decode("utf-8")
    hospital = "".decode("utf-8")
    for i in mdata:
        for j in i:
            
            #年龄
            agepat = '.*\d{1,}岁|年 龄.*\d{1,}|年齡.*\d{1,}|年龄.*\d{1,}|.*[男|女]\d{1,}'.decode("utf8")
            try:
                s = j.encode("utf-8")
                if re.search(agepat,s.decode("utf-8")):
                    age = re.search(agepat,s.decode("utf-8")).group(0)
                    age=re.compile('\d{1,}').search(age).group(0)
                    break
            except:
                continue
    for i in mdata:
        for j in i:
            
            #性别
            sexypat = '男|女'.decode("utf8")
            try:
                s = j.encode("utf-8")
                if re.search(sexypat,s.decode("utf-8")):
                    sexy = re.search(sexypat,s.decode("utf-8")).group(0)
                    break
            except:
                continue
            
    for i in mdata:
        for j in i:
            #检验日期
            check_timepat = '(?:采.*?时间|检验日期|本采集时间|采样时间|核收时间).*?(\d{2,4}.*?\d{1,2}.*?\d{1,2})'.decode("utf8")
            try:
                s = j.encode("utf-8")
                if re.search(check_timepat,s.decode("utf-8")):
                    check_time = re.search(check_timepat,s.decode("utf-8")).group(1)
                    break
            except:
                continue
    for i in mdata:
        for j in i:
            
            #报告日期
            report_timepat = '报.*?[时间|日期].*?(\d{2,4}.*?\d{1,2}.*?\d{1,2})'.decode("utf8")
            try:
                s = j.encode("utf-8")
                if re.search(report_timepat,s.decode("utf-8")):
                    report_time = re.search(report_timepat,s.decode("utf-8")).group(1)
                    break
            except:
                continue
    for i in mdata:
        for j in i:
            
            #检查人名称
            namepat = '姓名.([\\u4e00-\\u9fa5]{2,4})'.decode("utf8")
            try:
                s = j.encode("utf-8")
                if re.search(namepat,s.decode("utf-8")):
                    name = re.search(namepat,s.decode("utf-8")).group(1)
                    break
            except:
                continue
    for i in mdata:
        for j in i:
            
            #医院名称
            hospitalpat = '(.*医院)'.decode("utf8")
            try:
                s = j.encode("utf-8")
                if re.search(hospitalpat,s.decode("utf-8")):
                    hospital = re.search(hospitalpat,s.decode("utf-8")).group(0)
                    break
            except:
                continue

    dict_word={u'姓名':name,u'性别':sexy,u'年龄':age,u'检验日期':check_time,u'报告日期':report_time,u'医院名称':hospital}
    
    return filename,aa,dict_word
