from flask import Flask,send_file, redirect, url_for
import jira_backup

app = Flask(__name__)

content = '''
<textarea>
·功能说明：
将上传jira附件带有“备份”的Excel转换为json，Excel内容为主键加备份字符，可参考EBAO-9173
 

·执行当月数据备份任务
http://10.100.71.38:5000/

·执行yyyy-mm的数据备份任务
http://10.100.71.38:5000/yyyy-mm

·下载当月备份excel
http://10.100.71.38:5000/excel

·下载yyyy-mm的备份excel
http://10.100.71.38:5000/excel/yyyy-mm

·下载当月备份json
http://10.100.71.38:5000/json

·下载yyyy-mm的备份json
http://10.100.71.38:5000/json/yyyy-mm
</textarea>

'''

style = '''
<style>
    textarea {
      height: 1000px;
      width: 1800px;
      line-height: 1.4;
      font-size: 18px;
      text-align: center;
      color: #888;
    }
  </style>
'''  


@app.route('/')
def return_json():
    return jira_backup.get_json_info()


@app.route('/<date>', methods=['GET'])
def return_json_date(date):
    return jira_backup.get_json_info(date)


@app.route('/json', methods=['GET'])
def download_json():
    file_name = jira_backup.return_json_file()
    return send_file(file_name, as_attachment=True)

@app.route('/json/<date>', methods=['GET'])
def download_json_date(date):
    file_name = jira_backup.return_json_file(date)
    return send_file(file_name, as_attachment=True)

@app.route('/excel', methods=['GET'])
def download_excel():
    file_name = jira_backup.return_excel_file()
    return send_file(file_name, as_attachment=True)

@app.route('/excel/<date>', methods=['GET'])
def download_excel_date(date):
    file_name = jira_backup.return_excel_file(date)
    return send_file(file_name, as_attachment=True)

@app.route('/log', methods=['GET'])
def cat_log():
    file_name = r'log_file.txt'
    with open(file_name, "r") as f:
        lines = f.readlines()
        lines.reverse() 
    return '<style>' + str(lines) + '</style>' + style

@app.route('/dlog', methods=['GET'])
def download_log():
    file_name = r'log_file.txt'
    return send_file(file_name, as_attachment=True)



@app.route('/help', methods=['GET'])
def help():
    
    return content + style

if __name__=='__main__':
    app.run(host = '0.0.0.0', port = 5000)
