import docclass
import feedparser
import re
import xlsxwriter

def remove_html_tags(data):
  p = re.compile(r'<.*?>')
  return p.sub('', data)

def readfile(feed, fisherclassifier):
	# Get feed entries and loop over them
	title =[]
	guess =[]
	actual=[]
	f=feedparser.parse(feed)
	print(len(f))
	count = 0
	for entry in f['entries']:
		count = count + 1
		print(count)
		print ('-----')
		# Print the contents of the entry
		print ('Title: '+str(entry['title'].encode('utf-8')))
		print()
		fulltext = remove_html_tags(entry['title'])
		title.append(fulltext.replace(u"\u2019", "'").replace(u"\u2026", "...").replace(u"\u201c", "'").replace(u"\u201d", "'").replace(u"\u2122", "tm").replace(u"\u2013", "-"))
		fulltext = fulltext +" " +remove_html_tags(entry['summary'])
		# Print the best guess at the current category
		if count < 50:
			#print('Guess: '+str(fulltext.encode('utf-8')))		
			value = str(fisherclassifier.classify(fulltext))
			print('Guess: '+ value)
			guess.append(value)
			# Ask the user to specify the correct category and train on that
			temp = input('Enter Category:')
			print("value: ",temp)
			actual.append(temp)
			fisherclassifier.train(fulltext,temp)
		else:
			value1 = str(fisherclassifier.classify(fulltext))
			print(value1)
			guess.append(value1)		
		print()
	
	#input("Help")
	filename2 = r'\Table2.xlsx'
	workbook = xlsxwriter.Workbook(filename2)
	worksheet = workbook.add_worksheet()

	bold = workbook.add_format({'bold' : 1})

	#data headers
	worksheet.write('A1', 'Title', bold)
	worksheet.write('B1', 'Predicted', bold)
	worksheet.write('C1', 'Actual', bold)

	row = 1
	col = 0

	#throw data into 
	for name in title:
		worksheet.write_string(row, col, name)
		row += 1

	row1 = 1
	col1 = 1	
	for id in guess:
		worksheet.write_string(row1, col1, id)
		row1 += 1
		
	row1 = 1
	col1 = 2	
	for id1 in actual:
		worksheet.write_string(row1, col1, id1)
		row1 += 1
	workbook.close()
	
	return c2
		
#c1=docclass.classifier(docclass.getwords)
c2=docclass.fisherclassifier(docclass.getwords)
#c2 = readfile("http://gigabytedaily.blogspot.com/feeds/posts/default?max-results=100", c2)
value = 'y'
while value == 'y':
	temp = input("Enter a value:")
	temp1 = input("Enter Category:")
	print("Cprob",c2.cprob(temp,temp1))
	print("Fisher prob",c2.fisherprob(temp,temp1))
	value = input("Continue?")

