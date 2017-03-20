import paramiko 
def ssh_key(slave_ip):
        vm=paramiko.SSHClient()
        vm.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        vm.connect("10.45.207.82",username='root',password='shroot')
        cmd = "ssh-copy-id -i ~/.ssh/id_rsa.pub " + slave_ip
	print cmd
        stdin,stdout,stderr = vm.exec_command(cmd)
	print "In logs"
        for line in stdout.read().splitlines():
		print "In logs"
                print (line)
        vm.close()
	vm=paramiko.SSHClient()
	vm.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	vm.connect(slave_ip,username='root',password='shroot')
	cmd = "ssh-copy-id -i ~/.ssh/id_rsa.pub 10.45.207.82"
	print cmd
	stdin,stdout,stderr = vm.exec_command(cmd)
	for line in stdout.read().splitlines():
		print "In slave"
        	print (line)
	vmtransport = vm.get_transport()
        dest_addr = ("svc-1", 22)
        local_addr = (slave_ip, 22)
        vmchannel = vmtransport.open_channel("direct-tcpip", dest_addr, local_addr)
        jhost=paramiko.SSHClient()
        jhost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        jhost.connect('svc-1', username='litp-admin', password='12shroot', sock=vmchannel)
        print "Writing engine_A logs to file"
	try:
		stdin,stdot,stderr = jhost.exec_command("scp -o UserKnownHostsFile=~/.ssh/authorized_keys -o CheckHostIP=no -o StrictHostKeyChecking=no /var/VRTSvcs/log/engine_A.log root@10.45.207.82:/root/faultedlogs\n")
	        for line in stdot.read().splitlines():
	                print "In svc-1"
	                print (line)
	except:
		print "Unable to ssh"
	jhost.close()
	vm.close()

