import pandas as pd
import xlrd
import configparser
import json
import request_info
import re
import os
import datetime
from xlrd import xldate_as_tuple


def increase(i):
	i+=1
	return i

def excel_json(filepath,jira,jql_date):
    try:
            #filepath = r't_company_organ_备份.xls'
            book = xlrd.open_workbook(filepath)
    except Exception as e:
            print(str(e))

    #raw_data = pd.read_excel(filepath)
    #print(raw_data)
    sheet1 = book.sheets()[0]
    nrows = sheet1.nrows
    ncols = sheet1.ncols
    cell = sheet1.cell_value(0, 0)
    if len(jira)<0 or "-" not in jira: jira = 'EBAO-8888'
    if len(jql_date)<0: jql_date = '2088-12'
      
    base_name, file_extension = os.path.splitext(filepath)
    match = re.search(r't_.*[a-zA-Z]', base_name, re.IGNORECASE)
    if match:
        table = match.group()
        condition = sheet1.cell_value(0, 1)
        ctype = sheet1.cell(1, 1).ctype
        cell = sheet1.cell_value(1, 1)
        if ctype == 2 and cell % 1 == 0.0: 
                condition_value = [str(int(sheet1.cell_value(i, 1))) for i in range(1, nrows)]
        else:
                condition_value = [sheet1.cell_value(i, 1) for i in range(1, nrows)]
        fields_list= [sheet1.cell_value(0, i) for i in range(2, ncols)]
        value_list = [sheet1.row_values(i) for i in range(2, nrows)]
        serial_no = 0
        contents = []
        for i in range(1, nrows) : #去掉第一行title
            serial_no = increase(serial_no)
            records = []
            for j in range(2, ncols):
                    if sheet1.cell(i, j).ctype==2 and sheet1.cell_value(i, j)%1==0.0:
                            record  = request_info.Record(fields_list[j-2],str(int(sheet1.cell_value(i, j))))
                    elif sheet1.cell(i, j).ctype==3:
                            date_value = sheet1.cell_value(i, j)
                            
                            date_cell  = datetime.datetime(*xldate_as_tuple(date_value,0))
                            date_value = date_cell.strftime('%Y-%m-%d %H:%M:%S')
                            record  = request_info.Record(fields_list[j-2],date_value)
                    else:
                            record  = request_info.Record(fields_list[j-2],sheet1.cell_value(i, j))
                    records.append(record)
            condition = condition+"='"+str(condition_value[i-1])+"'" #从下标0开始
            content = request_info.Content(serial_no, condition, records)
            condition = sheet1.cell_value(0, 1)
            contents.append(content)


        request = request_info.Request(jira.split('-')[0],jql_date,serial_no,jira,table,contents)
        json_str = json.dumps(request, default=lambda o: o.__dict__, sort_keys=False, indent=2, ensure_ascii=False)
        #print(json_str)
        return json_str

    else :
        print("excel解析失败！")
        return

#excel_json('','','')




'''
方式1
-------------|-------------------------
t_policy_fee |	fee_id=12345678 and xxx   表、条件
-------------|-------------------------
fee_status   |	match_result	|  other  字段
-------------|------------------|-------
0	     |	      0         |  1      旧值
-------------|------------------|-------
2	     |        0         |  2      新值
-------------|------------------|-------
t_policy_prem|	prem_id=87654321|         ……
-------------|------------------|-------
match_result |	fee_status      |
-------------|------------------|-------
0	     |    0             |
-------------|------------------|-------
3	     |	  2


#方式1
    if cell and cell.startswith("t_") :

        #print(nrows,ncols)
        #print(sheet1.cell_type(nrows-1,ncols-1))
        #print(type(nrows))
        #获取所有修改表名
        table_list = [sheet1.cell_value(i*3, 0) for i in range(0, int(nrows/3))]
        #print(table_list)
        #获取所有条件
        condition_list= [sheet1.cell_value(i*3, 1) for i in range(0, int(nrows/3))]
        #print(sheet1.col_values(1))
        #获取表字段及修改数据

        serial_no = 0
        contents = []
        for i,table in zip(range(0,len(table_list)),table_list):
            fields_list = sheet1.row_values(i*3+1)
            value_list = sheet1.row_values(i*3+2)
            condition = sheet1.cell_value(i*3, 1)
            serial_no = increase(serial_no)
            records = []
            for field,value in zip(fields_list,value_list):
                if len(field):
                    record = request_info.Record(field,value)
                    records.append(record)

            content = request_info.Content(serial_no,jira,table,condition,records)
            contents.append(content)

'''    

