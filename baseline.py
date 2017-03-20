#!/usr/bin/python
import requests
from sys import argv
script,sprint=argv
page_source,pagesource_productset="",""
if "." in sprint[-2]:
	ISO="1."+str(47+int(sprint[-1:])-15)
else:
	ISO="1."+str(47+int(sprint[-2:])-15)
print ISO
url="https://cifwk-oss.lmera.ericsson.se/ENM/historicalContent/"+str(sprint)
data=requests.get(url)
page_source=page_source+str(data.text)
passed=page_source.count("passed.png")
failed=page_source.count("failed.png")
not_started=page_source.count("not_started.png")
in_progress=page_source.count("in_progress.png")
total=passed+failed+not_started+in_progress
print "***************************************************"
for i in range(1,total+1):
	productset=""
	productset=sprint+"."+str(i)
	url_productset="https://cifwk-oss.lmera.ericsson.se/ENM/content/"+sprint+"/"+productset
	data_productset=requests.get(url_productset)
	pagesource_productset=pagesource_productset+str(data_productset.text)
	ISO_index=pagesource_productset.find(ISO)
        info=page_source.rfind(productset)
	if i<10:
		if page_source[info+33:info+39]=="passed" or page_source[info+33:info+39]=="failed":
			print pagesource_productset[ISO_index:ISO_index+6]," ---> "+sprint+"." +str(i)," ---> ",page_source[info+33:info+39]
		elif page_source[info+33:info+39]=="not_st":
			print pagesource_productset[ISO_index:ISO_index+6]," --->"+sprint+"."+str(i)," ---> not started"
		else:
			print pagesource_productset[ISO_index:ISO_index+6]," --->"+sprint+"."+str(i)," ---> in progress"
	else:
		if page_source[info+34:info+40]=="passed" or page_source[info+34:info+40]=="failed":
                        print pagesource_productset[ISO_index:ISO_index+7]," --->"+sprint+"."+str(i)," ---> ",page_source[info+34:info+40]
                elif page_source[info+34:info+40]=="not_st":
                        print pagesource_productset[ISO_index:ISO_index+6]," --->"+sprint+"."+str(i)," ---> not started"
                else:
                        print pagesource_productset[ISO_index:ISO_index+7]," --->"+sprint+"."+str(i)," ---> in progress"

	info=page_source.rfind(productset)
        pagesource_productset=""
print "***************************************************"
print "Total Passed= ",passed
print "Total Failed= ",failed
print "Not Started= ",not_started
print "In Progress= ",in_progress
print "***************************************************"
#print total
