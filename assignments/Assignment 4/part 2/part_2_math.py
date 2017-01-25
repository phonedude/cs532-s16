import statistics
import re

if __name__ == "__main__":
	with open('followers_followers.txt') as f:
		data = f.read()
	data = map(int, re.findall('\d+', data))

	#print data
	#print 'mean: ', statistics.mean(data)
	#print 'standard deviation: ', statistics.stdev(data)
	#print 'median: ', statistics.median(data)
	print sorted(data)

	#data = sorted(data)

	#for elem in data:
	#	print elem