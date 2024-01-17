from cryptography.fernet import Fernet
import configparser
import calendar
import datetime
import os
import logging
import zipfile

def downloadAttachment(data,fpath):

    pdir = os.path.dirname(fpath)
    if not os.path.exists(pdir):
        os.makedirs(pdir)
    with open(fpath,'wb') as f:
        f.write(data)
        f.close()

    if os.path.exists(fpath):
        return
    else:
        print(filepath+"Download Attachment ERROR!")

# 获取第一天和最后一天
def getFirstAndLastDay(year,month):
    weekDay,monthCountDay = calendar.monthrange(year,month)
    firstDay = datetime.date(year,month,day=1).strftime('%Y-%m-%d')
    lastDay = datetime.date(year,month,day=monthCountDay).strftime('%Y-%m-%d')
    return firstDay,lastDay
        
        
def get_jira_key():
    config = configparser.ConfigParser()
    ini_file = os.path.dirname(os.path.abspath(__file__))
    config.read(ini_file+'/config.ini','utf-8')
    #cipher_key = Fernet.generate_key()
    cipher_key = config['DEFAULT']['cipher_key']
    cipher = Fernet(cipher_key)
    jira_key = config['DEFAULT']['jira_key']
    return cipher.decrypt(jira_key)

def encrypted():
    cipher_key = Fernet.generate_key()
    print(cipher_key)
    cipher = Fernet(cipher_key)
    text = b''
    encrypted_text = cipher.encrypt(text)
    print(encrypted_text)

def writeFile(fpath,content):
    pdir = os.path.dirname(fpath)
    if not os.path.exists(pdir):
        os.makedirs(pdir)
    file = open(fpath, 'w')
    file.write(content)
    file.close()



def getLogging():
    file_handler = logging.FileHandler('log_file.txt')
    stream_handler = logging.StreamHandler()
    # 设置日志级别为INFO
    logging.basicConfig(level=logging.INFO, handlers=[file_handler, stream_handler])
    #logging.info("This is a log message!")
    return logging

def compress_folder(folder_path, zip_name):
    pdir = os.path.dirname(zip_name)
    if not os.path.exists(pdir):
        os.makedirs(pdir)
    with zipfile.ZipFile(zip_name, 'w') as zip:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip.write(file_path, os.path.relpath(file_path, folder_path))


def compress_files(file_paths, zip_name):
    pdir = os.path.dirname(zip_name)
    if not os.path.exists(pdir):
        os.makedirs(pdir)    
    with zipfile.ZipFile(zip_name, 'w') as zip:
        for file_path in file_paths:
            zip.write(file_path, os.path.basename(file_path))



