import os
import sys
import time
import paramiko
from sys import argv
script,version,ms_IP= argv
with open('nodes.txt') as nodes_desc:
	lines=len(nodes_desc.readlines())
nodes_desc=open("nodes.txt","r+")
def netsim_login(server_name):
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(server_name,username='netsim', password='netsim')
                stdin, stdout, stderr = ssh.exec_command('cd..; inst/')
		sti,sto,ste=ssh.exec_command('pwd')
		o=sto.readlines()
		print o
                stdin1, stdout1, stderr1 = ssh.exec_command('echo ".show allsimnes" | /netsim/inst/netsim_shell |grep "arted"')
                error1=stderr1.readlines()
		if error1:
			sys.exit(0)
			print "Nodes are not started"
		stdin2, stdout2, stderr2 = ssh.exec_command(" echo '.show started' | /netsim/inst/netsim_shell | grep -i %s | awk '{print $2}' " %(node))
                output1=stdout1.readlines()
                output2=stdout2.readlines()
                error2=stderr2.readlines()
                ssh.close()
                ssh1=paramiko.SSHClient()
                ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                IP=str(output2[0])
		print IP
                ssh1.connect(ms_IP,username='root', password='12shroot')
		channel = ssh1.invoke_shell()
		channel.send('ssh -i .ssh/vm_private_key cloud-user@svc-3-mscmce\n')
		time.sleep(5)
		output=channel.recv(2048)
		vmtransport = ssh1.get_transport()
                dest_addr = (IP, 22)
                local_addr = (ms_IP, 22)
                vmchannel = vmtransport.open_channel("direct-tcpip", dest_addr, local_addr)
                jhost=paramiko.SSHClient()
                jhost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                jhost.connect(IP, username='netsim', password='netsim', sock=vmchannel)
if version=="5K":
	for line in range (0,18):
		node=nodes_desc.readline()
		node = node.replace('\n', '')
		if node[3:5]=="01" or node[3:5]=="03":
			server_name="ieatnetsimv6060-01"
		elif node[3:5]=="04" or node[3:5]=="06":
			server_name="ieatnetsimv6060-02"
                elif node[3:5]=="07" or node[3:5]=="09":
                        server_name="ieatnetsimv6060-03"
		else:
			print "Node doesn't exist"
		netsim_login(server_name)
		print line+1," of 18 success"
elif version=="15K":
	for line in range (0,36):
                node=nodes_desc.readline()
                node = node.replace('\n', '')
                if node[3:5]=="01" or node[3:5]=="03":
                        server_name="ieatnetsimv6060-01"
                elif node[3:5]=="04" or node[3:5]=="06":
                        server_name="ieatnetsimv6060-02"
                elif node[3:5]=="07" or node[3:5]=="09":
                        server_name="ieatnetsimv6060-03"
                elif node[3:5]=="10" or node[3:5]=="12":
                        server_name="ieatnetsimv6060-04"
                elif node[3:5]=="13" or node[3:5]=="15":
                        server_name="ieatnetsimv6060-05"
                elif node[3:5]=="16" or node[3:5]=="18":
                        server_name="ieatnetsimv6060-06"
                elif node[3:5]=="21":
                        server_name="ieatnetsimv6060-08"
                else:
                        print "Node doesn't exist"
		netsim_login(server_name)
		print line+1, " of 36 success"
else:
	print "Enter 5K or 15K"
