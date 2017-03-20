#Takes input from ips_file.txt. Pings each IP present in the file. All the IPs giving response are saved in ips_response.txt. The rest are saved in ips_no_response.txt
import sys
import subprocess
try:
	file_name=sys.argv[1]
	ips_file_descriptor=open(file_name,"r+")
	ips_response_desc=open("ips_response.txt","w+")
	ips_no_response_desc=open("ips_no_response.txt","w+")
	for line in ips_file_descriptor:
		command="ping -c 1 " + line
		proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
		(out, err) = proc.communicate()
		if "icmp_seq" in out:
			print "Got response from %s" %(line)
			ips_response_desc.write(line)
		else:
			print "No response from %s" %(line)
			ips_no_response_desc.write(line)
except:
        print "Execute as \npython ping_response.py <filename> \n\t\t where filename is the name of file which contains IP addresses"

