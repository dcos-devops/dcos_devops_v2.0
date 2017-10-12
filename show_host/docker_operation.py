#-*- coding:utf-8 -*-
# __author__='Hunter'

import paramiko

def show_exit_docker(hostname, port, username, password):
    paramiko.util.log_to_file("paramiko.log")
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    execmd="docker ps -a|grep Exit"
    s.connect(hostname=hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = s.exec_command (execmd)
    stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.
    dd = stdout.read()
    deal=dd.split('\n')
    dockerinfos=[]

    for info in deal:
        if len(info) ==0:
            continue
        ddd =  info.split()
        dockerinfo={}
        dockerinfo["ID"]=ddd[0]
        dockerinfo["NAME"]=ddd[-1]
        dockerinfos.append(dockerinfo)
    
    s.close()
    return dockerinfos

def del_docker(hostname, port, username, password, dockerid):
    paramiko.util.log_to_file("paramiko.log")
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    execmd="docker rm "+dockerid
    s.connect(hostname=hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = s.exec_command (execmd)
    stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.
    dd = stdout.read().split()[0]
    s.close()
    return dd
