import hashlib
from hashlib import md5
import os

fh = open("links",'r')
saveFile = open("uri_map",'ab')
# saveFile.write('{')
for line in fh:
	url=line
	url=url.replace('\n','')

	def computeMD5hash(message):
		m = hashlib.md5()
		m.update(message)
		return m.hexdigest()

	hashMessage = computeMD5hash(url)
	
	i = hashMessage + '\t' + url
        print i
	saveFile.write(i)
	saveFile.write('\n')
# saveFile.write('}')
saveFile.close()
