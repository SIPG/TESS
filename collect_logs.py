#!/usr/bin/python
import datetime,json,urllib,time,sys,pycurl,os,paramiko,pexpect,subprocess
from jenkinsapi.jenkins import Jenkins
from key_gen import ssh_key
KGB_Full="https://fem135-eiffel004.lmera.ericsson.se:8443/jenkins/view/KGB+N_Full/"
J = Jenkins(KGB_Full)
jobs= J.keys()
jobs_list=[]
for j in jobs:
        if "_Full_vApp_KGB+N" in j:
                jobs_list.append(j)
num_of_hours=2
current_date= datetime.datetime.today()
lastHourDateTime = current_date - datetime.timedelta(hours = 2)
base_past_date = lastHourDateTime.strftime('%Y-%m-%d %H:%M:%S')
print "current_date: " , current_date
print "base_past_date: ",  base_past_date
print "================"

def get_ip(url):
        class ContentCallback:
                def __init__(self):
                        self.contents = ''

                def content_callback(self, buf):
                        self.contents = self.contents + buf

        t = ContentCallback()
        curlObj = pycurl.Curl()
        curlObj.setopt(curlObj.URL, url)
        curlObj.setopt(curlObj.WRITEFUNCTION, t.content_callback)
        curlObj.perform()
        curlObj.close()
        lines = t.contents.splitlines()
        for line in lines:
                if "#Geteway IP: " in line:
                        return line[13:]


def write_logs(slave_ip,list_offline):
        ssh_key(slave_ip)
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
        try:
                stdin,stdout,stderr = jhost.exec_command('scp -o UserKnownHostsFile=/dev/null -o CheckHostIP=no -o StrictHostKeyChecking=no /var/VRTSvcs/log/engine_A.log root@10.45.207.82:/root/faultedlogs\n')
                for line in stdout.read().splitlines():
                        print (line)

        except:
                print "Unable to copy"

        jhost.close()
        vm.close()
        vm.connect(hostname="10.45.207.82", username="root", password="shroot")

def get_faulted_services(slave_ip):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
                ssh.connect(hostname=slave_ip,username='root', password='shroot')
                channel = ssh.invoke_shell()
                lst,list_offline,results=[],[],""
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
                write_logs(slave_ip,list_offline)
        except:
                pass

for job in jobs_list:
        my_job = J.get_job(job)
        job_link=KGB_Full+"job/"+job+"/api/json?pretty=true"
        response_temp = urllib.urlopen(job_link)
        response = json.loads(response_temp.read())
        jobName = response["lastFailedBuild"]
        if jobName != None:
                lastJobFailed = jobName[u'number']
                failedJobLink = KGB_Full+"job/"+job+"/"+str(lastJobFailed)
                failedJobJson = failedJobLink+"/api/json?pretty=true"
                responseJob_temp = urllib.urlopen(failedJobJson)