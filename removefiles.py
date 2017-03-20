import os,time,datetime
import shutil
def get_server_list(directory):
	global server_list
	for i in os.listdir(directory):
		a=os.stat(os.path.join(directory,i))
		server_list.append(i)
def get_information(directory):
    time_created_list=[]
    files_list=[]
    for i in os.listdir(directory):
        a = os.stat(os.path.join(directory,i))
	files_list.append(i)
	t=time.strptime(time.ctime(a.st_ctime), "%a %b %d %H:%M:%S %Y")
	d=time.localtime()
        time_created_list.append(t)
        d0=datetime.date(t.tm_year,t.tm_mon,t.tm_mday)
	d1=datetime.date(d.tm_year,d.tm_mon,d.tm_mday)
	delta=d1-d0
#	print directory," created on ",d0," was ",delta.days," days old"
	if delta.days>=7:
		path=directory+"/"+i
		print "Deleting ",path
		shutil.rmtree(path)		
server_list=[]
get_server_list("/root/scripts/xbalbem/harsha/logs")
for i in server_list:
	str="/root/scripts/xbalbem/harsha/logs/"+i
	get_information(str)
