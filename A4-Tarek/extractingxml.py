def readingxml():
	i = 0
	with open('xml.txt', 'r') as file:
		with open('freindscount.txt','w') as f:
			for line in file:
				if '"friend_count"' in line:
					i = i +1
					counter = str(int(i))
					f.write(line)