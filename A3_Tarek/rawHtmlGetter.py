import os 
import subprocess
destination  = "html"
i = 1
with open('urls.txt') as fil:
	for line in fil:
			s = line.strip('\n')
			proc = subprocess.Popen(["lynx -source "+ '"'+s+'"' +"> " + destination + "{0}".format(i)+".txt"], stdout=subprocess.PIPE, shell=True)
			(out, err) = proc.communicate()
			i = i + 1