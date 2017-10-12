#-*- coding:utf-8 -*-
# __author__='Hunter'

import paramiko

def show_log(hostname, port, username, password, execmd):
    paramiko.util.log_to_file("paramiko.log")
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname=hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = s.exec_command (execmd)
    stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.
    dd = stdout.read()
    deal =  dd.split("\n")
    fileinfos=[]
    for info in deal:
        if len(info) ==0:
            continue
        ddd =  info.split("\t")
        fileinfo={}
        fileinfo["size"]=ddd[0]+'M'
        fileinfo["filename"]=ddd[1]
        fileinfos.append(fileinfo)
    
    s.close()
    return fileinfos

def del_log(hostname, port, username, password, loginfo):
    paramiko.util.log_to_file("paramiko.log")
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    execmd = "rm -rf %s" % loginfo
    s.connect(hostname=hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = s.exec_command (execmd)
    stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.
    dd = stdout.read()
    s.close()
    return dd

def empty_log(hostname, port, username, password, loginfo):
    paramiko.util.log_to_file("paramiko.log")
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #Todo
    #判断选择的问题是否合规,是不是.log结尾
    if loginfo[-4:]!='.log':
        return 'this is not a logfile end with .log'

    execmd = "> %s" % loginfo
    s.connect(hostname=hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = s.exec_command (execmd)
    stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.
    dd = stdout.read()
    s.close()
    return dd
    
def test():
    hostname = '20.26.33.32'
    port = 22
    username = 'root'
    password = '20172Epc'
    execmd = "du -m /data/logs/*/*  | sort -nr | head -n 10"
    show_log(hostname, port, username, password, execmd)
    del_log(hostname, port, username, password, "/data/logs/resource-center-dev/resource-center-dev-0aa53c2136be-20171010.log") 
    empty_log(hostname, port, username, password, "/data/logs/resource-center-dev/resource-center-dev-0aa53c2136be-20171010.log") 

