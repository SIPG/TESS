#!/usr/bin/python
import paramiko,sys,subprocess

cluster = sys.argv[1]

if(cluster == '341'):
	cluster_ip = '10.43.250.159'
elif(cluster == '402'):
	cluster_ip = '141.137.149.45'
elif (cluster == '403'):
        cluster_ip = '141.137.149.141'
else:
	print "This cluster is not a CDL Cluster"
	sys.exit(1)

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(cluster_ip, username='root',password='12shroot')

transport = client.get_transport()
dest_addr = ('svc-1', 22) 
local_addr = (cluster_ip, 22) 
channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)

client2 = paramiko.SSHClient()
client2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#client2.load_host_keys('/root/.ssh/known_hosts') 
client2.connect('svc-1', username = 'litp-admin', password = '12shroot', sock = channel)

stdin, stdout, stderr = client2.exec_command("cat /var/VRTSvcs/log/engine_A.log | grep 'clean completed successfully'")

print stdout.read()

client2.close()
client.close()
