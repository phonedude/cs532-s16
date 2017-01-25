from urlparse import urlparse

unsortedFile = open('UnsortedURL.txt', 'a')
parserFile = open('Parsed.txt', 'w')
condensedFile = open('condensed.txt', 'w')

with open('UnsortedURL.txt') as f:
    lines = f.readlines()
    lines = [x.strip('\n') for x in lines]

for line in lines:
    o = urlparse(line)
    #print o.netloc
    parserFile.write(o.netloc) 
    parserFile.write("\n")
parserFile.close()

parserFile = open('Parsed.txt', 'a')
with open('Parsed.txt') as z:
    parser = z.readlines()
    parser = [x.strip('\n') for x in parser]
parserFile.close()
parsing = list(set(parser))
for parsed in parsing:
    print parsed
    condensedFile.write(parsed)
    condensedFile.write("\n")

condensedFile.close()
unsortedFile.close()




#unsortedFile.write(url['expanded_url']) 
#unsortedFile.write("\n")






#for secondline in line:
#	    z = urlparse(secondline)
#	    if z.netloc == o.netloc:
#		    secondline = ''
#            print 'working'