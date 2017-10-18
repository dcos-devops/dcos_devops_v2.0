#-*- coding:utf-8 -*-

import paramiko

def show_exit_docker(hostname, port, username, password):
    paramiko.util.log_to_file("paramiko.log")
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    execmd="docker ps -a|grep -E 'Exit|Created'"
    s.connect(hostname=hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = s.exec_command (execmd)
    stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.
    dd = stdout.read()
    deal=dd.split('\n')
    dockerinfos=[]

    for info in deal:
        if len(info) ==0:
            continue
        ddd =  info.split('  ')
        eee = []
        for i in ddd:
            if i!='':
                eee.append(i.strip())
        dockerinfo={}
        dockerinfo["ID"]=eee[0]
        dockerinfo["IMAGE"]=eee[1]
        dockerinfo["CREATED"]=eee[3]
        dockerinfo["STATUS"]=eee[4]
        dockerinfos.append(dockerinfo)
    
    s.close()
    return dockerinfos

def del_docker(hostname, port, username, password, dockerid):
    '''
       删除处于exit和create的容器。 远程调用docker rm -f -v 
       @dockerid: 容器的id
    '''
    paramiko.util.log_to_file("paramiko.log")
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    execmd="docker rm -f -v "+dockerid
    s.connect(hostname=hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = s.exec_command (execmd)
    stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.
    dd = stdout.read().split()[0]
    s.close()
    return dd

def del_dockers(hostname, port, username, password):
    paramiko.util.log_to_file("paramiko.log")
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    execmd="docker ps -a|grep -E 'Exit|Created'|awk '{print $1}'|xargs docker rm"
    s.connect(hostname=hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = s.exec_command (execmd)
    stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.
    dd = stdout.read().split()
    s.close()
    return dd
