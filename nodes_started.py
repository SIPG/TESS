import os
import paramiko
from sys import argv
server_name = "ieatnetsimv6060-01"
ms_IP="141.137.149.141"
#script,server_name, total_servers = argv
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(server_name,username='netsim', password='netsim')
stdin, stdout, stderr = ssh.exec_command('cd..; inst/')
stdin1, stdout1, stderr1 = ssh.exec_command('echo ".show allsimnes" | /netsim/inst/netsim_shell |grep "arted"')
stdin2, stdout2, stderr2 = ssh.exec_command(" echo '.show started' | /netsim/inst/netsim_shell | grep -i LTE02ERBS00001 | awk '{print $2}' ")
output1=stdout1.readlines()
output2=stdout2.readlines()
error1=stderr1.readlines()
error2=stderr2.readlines()
ssh.close()
ssh1=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
IP=str(output2[0])
ssh.connect(ms_IP,username='root', password='12shroot')
ssh.invoke_shell('ssh -i .ssh/vm_private_key cloud-user@svc-3-mscmce')
IP_server="ssh netsim@"+IP
ssh.invoke_shell(IP_server)
