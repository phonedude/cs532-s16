def extractingnumber():
	with open('freindscount.txt','r') as f ,open('numbers_count.txt ','w') as n:
			for line in f:
				temp="".join(re.findall(r'\d+',line)) +"\n"
				n.write(temp)