import os
import subprocess
pth = '/Users/mohamedshaaban/Desktop/Tarek_Fouda/'
text_files=[f for f in os.listdir(pth) if f.endswith('.txt.proccesed')]
fileindex= 0
numberoffiles = 0
while (fileindex<len(text_files)):
	#with open(text_files[i]) as fil:
		wordcount=0
		for line in open(text_files[fileindex]):
 			if "market" in line:
 				wordcount = wordcount+1
 		if(wordcount>0):
 			numberoffiles = numberoffiles +1		
		print text_files[fileindex] + " Processed file has word (market): " + "{0}".format(wordcount) + " times"
		fileindex=fileindex+1
print "Number of Total files having the word is: " + "{0}".format(numberoffiles)