import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(slave_ip,username='root', password='shroot')
channel = ssh.invoke_shell()
channel.send("ssh ms-1 '/opt/ericsson/enminst/bin/vcs.bsh --groups | grep OFFLINE &' | awk '{print $2}'\n")

