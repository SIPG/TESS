#!/usr/bin/python
import os,time
import paramiko
import sys
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("141.137.111.149",username='root', password='shroot')
channel = ssh.invoke_shell()
lst,list_offline,results=[],[],""
#channel.send("ssh ms-1 '/opt/ericsson/enminst/bin/vcs.bsh --groups | grep FAULTED &'\n")
channel.send("ssh ms-1 '/opt/ericsson/enminst/bin/vcs.bsh --groups | grep OFFLINE &' | awk '{print $2}'\n")
while not channel.recv_ready():
    time.sleep(10)
results += channel.recv(2048)
lst=results.splitlines()
for i in range(0,len(results.split('\n'))+2):
	head, sep, tail = lst[i].partition('Grp_CS_svc_cluster_')
	list_offline.append(tail)
list_offline = [item for item in list_offline if item != '']
print "****************************************************"
print list_offline
