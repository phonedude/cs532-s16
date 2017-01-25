# Tarek Fouda
# This program takes a website as a command line argument
# and extract all the links that are PDFs and show each size.
import urllib2
import BeautifulSoup
import sys
import re
from fpdf import FPDF
print "Please enter the website"
var = raw_input()
#print var
#def process(var):
 #  website=urllib2.urlopen(var)
  # html=website.read()
   #links= re.findall("((http|ftp)s>://.*?)",html)
   #print links
def extractingUrls(var):
	
    print "hi"
    if var[0:4]!="http":
        var="http://" + var
    f=(urllib2.urlopen(var)).read()
    k=re.findall('(src|href)="(\S+)"',f)	
    k=set(k)
    print "The Links are:"
    #k is a two dimensional array where the first column is (src or href) and the second
    #is the link itself which we will print it.
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 10)	
    for x in k:
        if len(x[1])>2:
            try:
              ah = var[7:]
              #print ah
              ba = ah.partition("/")[0]	
              #print ba +"ajaj"	
              #print x[1]			  
              if x[1][0:4]=="http":
                response = urllib2.urlopen(x[1])
                if response.info()["Content-Type"] == 'application/pdf':
                  print x[1]+" the size of the pdf file is "+ response.info()["Content-Length"]       
              elif x[1][-4:] ==".pdf" and x[1][0:4]!="http" :
                if x[1][0:1] == "/":
                  #print ba + x[1]
                  response = urllib2.urlopen("http://" + ba+x[1])
                  if response.info()["Content-Type"] == 'application/pdf':
                    print ba + x[1]+" the size of the pdf file is "+ response.info()["Content-Length"]  
                else:
                  #print ba + x[1]
                  response = urllib2.urlopen("http://" + ba+'/'+x[1])
                  if response.info()["Content-Type"] == 'application/pdf':
                    print ba +'/'+ x[1]+" the size of the pdf file is "+ response.info()["Content-Length"]  
            except:
              pass			
			#print response.info()
            #print "The size is: ", response.code
extractingUrls(var)





   
