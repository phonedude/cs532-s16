import re
import math
import statistics


def readingxml():
	i = 0
	with open('xml.txt', 'r') as file:
		with open('freindscount.txt','w') as f:
			for line in file:
				if '"friend_count"' in line:
					i = i +1
					counter = str(int(i))
					f.write(line)


def extractingnumber():
	with open('freindscount.txt','r') as f ,open('numbers_count.txt ','w') as n:
			for line in f:
				temp="".join(re.findall(r'\d+',line)) +"\n"
				n.write(temp)


def calculateMean():
	lis=[]
	with open ('numbers_count.txt ','r') as nc:
		total = sum(int(x)
		for line in nc
		for x in line.split())
		#print ("Total = ",total)
	mean = total /154 
	print ("Mean = ",mean)
	return mean



def calculateSD(var):
	ls=[]
	with open ('numbers_count.txt ','r') as nc:
		for line in nc:
			no = int(line) - var
			no2= no *no
			ls.append(no2)
		sqTotal = sum(ls)
		Mean= sqTotal/ var
		sd= math.sqrt(sqTotal)
		print ("STD = ",sd) 


 



def calculateMedian():
	ls=[]
	with open ('numbers_count.txt ','r') as n:
		for line in n:
			ls.append(line.strip('\n'+''))
		ls =list(map(int, ls))
		median = statistics.median(ls)
		print ("Median = ",median)
readingxml()
extractingnumber()
mean = calculateMean()
calculateSD(mean)
calculateMedian()