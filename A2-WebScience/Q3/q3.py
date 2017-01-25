import re
from sys import argv
txt = open("EstimatedTime.txt")
#print txt.read()
x=re.findall(r'\"(.+?)\"',txt.read())
lengthOfList = len(x)
counter=0
while(counter < lengthOfList):
	check2 = x[counter-2]
	check = x[counter]
	if(check[0].isdigit()):
		print check
		if(check2[0] == "h"):
			print check2
	counter = counter +1