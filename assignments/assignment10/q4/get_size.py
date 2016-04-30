import os, sys

savefile = open('new_processed_size', 'a')
path = "html/processed/"

for filename in os.listdir(path):
	filepath = os.path.join(path, filename)
	size = os.path.getsize(filepath)
	savefile.write(str(size))
	savefile.write('\n')
	print size
	
savefile = open('new_raw_size', 'a')
path = "html/raw/"

for filename in os.listdir(path):
	filepath = os.path.join(path, filename)
	size = os.path.getsize(filepath)
	savefile.write(str(size))
	savefile.write('\n')
	print size
	
savefile = open('old_processed_size', 'a')
path = "old/html/processed/"

for filename in os.listdir(path):
	filepath = os.path.join(path, filename)
	size = os.path.getsize(filepath)
	savefile.write(str(size))
	savefile.write('\n')
	print size

savefile = open('old_raw_size', 'a')
path = "old/html/raw/"

for filename in os.listdir(path):
	filepath = os.path.join(path, filename)
	size = os.path.getsize(filepath)
	savefile.write(str(size))
	savefile.write('\n')
	print size