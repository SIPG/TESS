import paramiko
def func(slave_ip):
	vm=paramiko.SSHClient()
        vm.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        vm.connect(hostname=slave_ip,username='root',password='shroot')
        vmtransport = vm.get_transport()
        dest_addr = ("svc-1", 22)
        local_addr = (slave_ip, 22)
        vmchannel = vmtransport.open_channel("direct-tcpip", dest_addr, local_addr)
        jhost=paramiko.SSHClient()
        jhost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        jhost.connect(hostname='svc-1', username='litp-admin', password='12shroot', sock=vmchannel)
        print "Writing engine_A logs to file"
	log, lines_list="",[]
        try:
                stdin,stdout,stderr = jhost.exec_command('cat /var/VRTSvcs/log/engine_A.log\n')
                for line in stdout.read().splitlines():
			log=log+line+"\n"
		print len(log)
		quo = len(log)/100000
		rem = len(log)%100000
        except:
                print "Unable to copy"

        jhost.close()
        vm.close()
        vm.connect(hostname="10.45.207.82", username="root", password="shroot")
        try:
		for i in range (0,quo):
			cmd = 'echo "' + log[i*100000:(i+1)*100000] + '" >> /root/faultedlogs/engin_A.log\n'
			print cmd
       		        stdin,stdout,stderr = vm.exec_command(cmd)
		cmd = 'echo "' + log[(i+1)*100000:((i+1)*100000)+rem] + '" >> /root/faultedlogs/engin_A.log\n'
		print cmd
        except:
                print "Can't copy"

func("141.137.111.212")
