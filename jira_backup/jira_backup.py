from jira import JIRA
import os.path
import time
import datetime
import calendar
import configparser
import mycypher
import sys
import pyexcel
import os
from django.http import HttpResponse
from django.shortcuts import render


#jira数据维护备份功能


#配置获取JIRA
config = configparser.ConfigParser()
config.read('config.ini','utf-8')
EBAO_PROJECT = config['DEFAULT']['EBAO_PROJECT']
AttachmentDir = config['DEFAULT']['AttachmentDir']
JsonDir = config['DEFAULT']['JsonDir']
attachment_key = config['DEFAULT']['attachment_key']
jira_url = config['DEFAULT']['jira_url']
username = config['DEFAULT']['username']
project = config['DEFAULT']['project']

jira = JIRA(jira_url, auth=(username, str(mycypher.get_jira_key().decode("utf-8"))))
logging = mycypher.getLogging()
current_time = datetime.datetime.now()
year_month = ""

def test_jira():
    issue = jira.issue('EBAO-9072')
    #print(issue.key, issue.fields.attachment, issue.fields.comment)
    comments = jira.comments(issue)
    comment_list = []
    for comment in comments:
        comment_list.append(comment.body)

    print(comment_list)
    
    
def search_issues(date1):

    year_month = date1
    year,month = get_jql_date(date1)
    firstDay,lastDay = mycypher.getFirstAndLastDay(int(year),int(month))
    JQL = 'project in ('+ project+') AND issuetype = 运维 AND 是否数据修改 = 是 AND created >= '+firstDay+' AND created <= '+lastDay
    logging.info("开始处理时间========"+str(current_time)+"========")
    logging.info('JQL = ' + JQL)
    issue_list = jira.search_issues(JQL, maxResults=-1)
    #print(issue_list)
    #for issue in issue_list:
        # 打印每个 issue 的 key
        #logging.info(issue.key)
    return issue_list

    
def get_jql_date(year_month):
    try:
        if len(year_month) == 0:
            year = datetime.date.today().year
            month = datetime.date.today().month
        else:
            year,month = year_month.split('-')
    except:
        print('直接回车默认为当前月份，或输入正确日期:yyyy-mm')
        return
    return int(year),int(month)


def get_issue(jira_no):
    
    return jira.issue(jira_no)
    

#根据日期下载附件-启动程序
def start_program():
    rjira = ""
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        print("输入的日期是：", arg)
    else:
         arg = ""
    issue_list = search_issues(arg)
    for issue in issue_list:
        get_attachment(issue.key)



#接口调用-传入日期
def get_json_info(date=""):
    rjira = ""
    issue_list = search_issues(date)
    for issue in issue_list:
        get_attachment(issue.key)
        rjira = rjira + ", " + issue.key 
    result = "执行完成!\n 数据维护的JIRA包括：" +  rjira
    return result


#获取jira号下的备注
def get_comments(jira_no):
    issue = jira.issue(jira_no)
    #print(issue.key, issue.fields.attachment, issue.fields.comment)
    comments = jira.comments(issue)
    comment_list = []
    for comment in comments:
        comment_list.append(comment.body)

    print(comment_list)
    return comment_list
    

#根据jira号下载备份附件转为json
def get_attachment(jira_no):

    if os.path.exists(AttachmentDir) == False:
        os.makedirs(AttachmentDir)

    issue = get_issue(jira_no)
    attachment_list = issue.fields.attachment
    #print(attachment_list)
    #print(attachment_list[0].id)
    num = 0
    year,month = get_jql_date(year_month)
    if int(month/10)==0:
        month = "0"+str(month)
    date_path = str(year)+"-"+str(month)
    for attachment in attachment_list:
        #filename = jira_no + '_'+ str(calendar.timegm(time.gmtime())) + '_'+ attachment.filename
        #处理包含关键字的excel
        attName = attachment.filename
        if(attName.__contains__(attachment_key) and attName.__contains__(".xls")):
            num = num + 1
            filename = jira_no + '_'+ attachment.id + '_'+ attName
            fpath = os.path.join(AttachmentDir, date_path, filename)
            mycypher.downloadAttachment(attachment.get(), fpath)
            #excel转json
            json_str = pyexcel.excel_json(fpath,jira_no,date_path)
            #存储json
            base_name, file_extension = os.path.splitext(fpath)
            file_name = os.path.basename(base_name)
            file_name = os.path.join(JsonDir, date_path, file_name)
            mycypher.writeFile(file_name+"_"+str(num)+".json",json_str)

    # 压缩json
    folder_path = os.path.join(JsonDir, date_path)
    zip_name = folder_path+"-json.zip"
    mycypher.compress_folder(folder_path, zip_name)

    # 压缩excel
    folder_path = os.path.join(AttachmentDir, date_path)
    zip_name = folder_path+"-excel.zip"
    mycypher.compress_folder(folder_path, zip_name)

def return_json_file(date=""):
    year,month = get_jql_date(date)
    if int(month/10)==0:
        month = "0"+str(month)
    date_path = str(year)+"-"+str(month)
    filename = date_path+"-json.zip"
    file_path = os.path.join(JsonDir, filename)
    return file_path

def return_excel_file(date=""):
    year,month = get_jql_date(date)
    if int(month/10)==0:
        month = "0"+str(month)
    date_path = str(year)+"-"+str(month)
    filename = date_path+"-excel.zip"
    file_path = os.path.join(AttachmentDir, filename)
    return file_path

    
if __name__=='__main__':
    print("开始运行......")
    #test_jira()
    #按jira号下载附件
    #get_attachment('EBAO-9066')
    #按月下载备份附件
    #search_issues("2024-01")
    #search_issues()

    start_program()
    #get_attachment("EBAO-9129")
    
    #search_issues()
    #print(getFirstAndLastDay(2023,2))
    #year_month = '2023-12'
    #year,month = year_month.split('-')
    #print(year,month )
    #search_issues('11')
    #search_issues('2024-02')

    #附件路径，jira号，统计时间
    #pyexcel.excel_json('','','')
    





'''

    list = [1,2,3]
    for i in range(1,len(list)):
        print(i)
    #print(jira.projects()) #权限下的项目列表
    #print(project.key, project.name, project.raw)

    #issue = jira.issue(EBAO_PROJECT+'-9072')
    #print(issue.key, issue.fields.summary, issue.fields.reporter, issue.raw) 
    print(issue.key, issue.fields.attachment, issue.fields.comment) 
    print(jira.comments(issue))
    print(issue.fields.description) #问题描述
    print(issue.fields.issuetype) #类型
    print(issue.fields.attachment.id)
    print(jira.attachment(317767).filename)
    print(jira.attachment(317767).content)

    #print('xxxx备x份.xls'.__contains__("备份"))
    #issues，默认固定返回50个数据。startAT 和 maxResults 可以实现分页查询效果。
    issue_list = jiraClinet.search_issues('JQL语句',startAT=0,maxResults=False)

    for issue in issue_list:
        # 打印每个 issue 的 key
        print(issue.key)
        
'''












    
