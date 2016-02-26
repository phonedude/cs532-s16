import statistics
import re
if __name__ == "__main__":
	with open('updated_friend_counts.txt') as f:
		data = f.read()
	data = map(int, re.findall('\d+', data))

	#print data
	print 'mean: ', statistics.mean(data)
	print 'standard deviation: ', statistics.stdev(data)
	print 'median: ', statistics.median(data)