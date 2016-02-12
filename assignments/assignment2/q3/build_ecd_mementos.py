#! /usr/bin/python

if __name__ == '__main__':
	with open('site_ecd_all') as ecdfile:
		ecdmap = dict([line.rstrip('\n').split() for line in ecdfile])
	with open('site_mementos') as memfile:
		mementos = dict([line.rstrip('\n').split() for line in memfile if line.rstrip('\n').split()[1] != '0'])
	with open('ecd_mementos', 'w') as outfile:
		outfile.write('ECD Mementos\n')
		for uri, mem in mementos.iteritems():
			try:
				outfile.write('{} {}\n'.format(ecdmap[uri], mem))
			except KeyError as e:
				print('{}\n'.format(e))
