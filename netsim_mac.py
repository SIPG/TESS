#Takes two arguments (first server name and total no of servers), get their MAC address and write them in netsim_mac.txt
import paramiko
from sys import argv
try:
	script,server_name, total_servers = argv
	server_list=[]
	netsim_mac_descriptor=open("netsim_mac.txt","w+")
	Headings="\t"+"   Server Name"+"\t\t"+"   MAC"+"\n"
	netsim_mac_descriptor.write(Headings)
	for i in range(0,int(total_servers)):
	        ssh = paramiko.SSHClient()
	        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	        ssh.connect(server_name,username='netsim', password='netsim')
	        stdin, stdout, stderr = ssh.exec_command("ip link show eth0 | grep link/ether | awk '{print $2}'")
	        output=stdout.readlines()
		print output
		print output[0]
		ip_server_name_MAC="\t"+server_name+"\t"+str(output[0])
	       	netsim_mac_descriptor.write(ip_server_name_MAC)
	        ssh.close()
	        temp=int(server_name[-2:])+1
       		temp=str(temp)
        	if int(temp)<=9:
        	        temp="0"+temp
        	server_name=server_name[0:len(server_name)-2]+temp
	print "Your output is in netsim_mac.txt"
except:
	print "Execute Command as: \npython netsim_mac.py <first server name> <total number of servers>"

