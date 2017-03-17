#!/usr/bin/python
import urllib,json,time,sys,urllib2,cookielib,re
from getpass import getpass

args = sys.argv[1:]
if(len(args) < 1): url=raw_input("Enter job url: ")

p = re.compile('^[789]\d{9}$')

numbers = []
jobLinks = []
#number = "9494575042"

for arg in args:
	if(p.match(arg)):
		numbers.append(arg)
	else: 
		jobLinks.append(arg)

#if( len(numbers) == 0): numbers.append("9494575042")
if( len(numbers) == 0):
	numbers.append("9494575042")
#global jobLinks
#getLinks(jobLinks)
def getLinks(jobLinks):
	links=[]
        for url in jobLinks:
                if "consoleFull" in url:
                        links.append(url[:-11]+"api/json?pretty=true")
                elif "console" in url:
                        links.append(url[:-7]+"api/json?pretty=true")
                else:
                        links.append(url+"api/json?pretty=true")
	return links

def sendAlerts(msg):
	for num in set(numbers):
		message(msg,num)
		#sys.exit(1)

#links=getLinks(jobLinks)
#print links

def message(msg,num):
	username = "9494575042"
	passwd = "S9628P"
	#number = "9494575042"
	number = num
	message = msg
    #Logging into the SMS Site
	url = 'http://site24.way2sms.com/Login1.action?'
	data = 'username='+username+'&password='+passwd+'&Submit=Sign+in'
    #For Cookies:
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # Adding Header detail:
	opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')]
	try:
	       usock = opener.open(url, data)
	except IOError:
	        print "Error while logging in."
	        sys.exit(1)
	jession_id = str(cj).split('~')[1].split(' ')[0]
	send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
	send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+number+'&message='+message+'&msgLen=136'
	opener.addheaders = [('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]

	try:
	       sms_sent_page = opener.open(send_sms_url,send_sms_data)
	except IOError:
       		print "Error while sending message"

	#sys.exit(1)
	print "SMS has been sent."

print "Alerts will be sent to "
print numbers
links=getLinks(jobLinks)
#activeJobLinks = links
while True:
	activeJobLinks = links
	print activeJobLinks
	if(len(activeJobLinks) < 1):
		sys.exit(1)
	links = []
	for url_env in activeJobLinks:
		response_env = urllib.urlopen(url_env)
		data_env = json.loads(response_env.read())
		jobName = data_env["fullDisplayName"].replace("_", " ")
		result = data_env["result"]
		building = data_env["building"]
		if result == "SUCCESS" and not building:
			msg = jobName + " - Success"
			print msg
			sendAlerts(msg)
			#sys.exit(1)
		elif result =="FAILURE" and not building:
			msg = jobName + " - Failure"
			print msg
			sendAlerts(msg)
			#sys.exit(1)
		else:
			links.append(url_env)
			print jobName + " Job Ongoing"
	#activeJobLinks = links
	print "Running Jobs - " + str(len(activeJobLinks))
	time.sleep(30)

#MTG
