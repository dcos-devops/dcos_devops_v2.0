#-*- coding:utf-8 -*-
# __author__='Hunter'

import paramiko

def show_log(hostname, port, username, password, execmd):
    '''
    展示日志文件。目前定位为/data/logs下。同时大小格式统一标准为M
    @hostname:要远程的主机IP，
    @port:能够ssh的端口，一般为22
    @username,password：用户名和密码
    @execmd：要执行的命令
    '''
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
    '''
    @loginfo:日志文件的绝对路径
    '''
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
    '''
    写空日志
    '''
    paramiko.util.log_to_file("paramiko.log")
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #Todo
    #判断选择的问题是否合规,是不是.log结尾
    #if loginfo[-4:]!='.log':
    #    return 'this is not a logfile end with .log'
    # 取消判断,生产上.tar.gz也能写空，达到清理空间的目的。同时mesos的日志是不规范的。
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

