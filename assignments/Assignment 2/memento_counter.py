from datetime import datetime
import dateutil.parser
import re
import StringIO
import urllib
import urllib2
from pprint import pprint

#==================================================================
# KEYWORDS
#==================================================================

#==================================================================
# REGULAR EXPRESSIONS
#==================================================================

tokenizer = re.compile('(<[^>]+>|[a-zA-Z]+="[^"]*"|[;,])\\s*')

#==================================================================
class TimeMap(object):
#==================================================================

    def __init__(self, uri=None, data=None):
        self.original      = None
        self.timebundle    = None
        self.timegate      = None
        self.timemap       = None
        self.first_memento = None
        self.last_memento  = None
        self.mementos      = {}
        self.__tokens = TimeMapTokenizer(uri, data)
        link = self.get_next_link()
        while link != None:
            if link[0] == 'memento':
                self.mementos[link[1]] = link[2]
            elif link[0] == 'original':
                self.original = link[2] if link != None else None
            elif link[0] == 'timebundle':
                self.timebundle = link[2] if link != None else None
            elif link[0] == 'timegate':
                self.timegate = link[2] if link != None else None
            elif link[0] == 'timemap':
                self.timemap = link[2] if link != None else None
            elif link[0] == 'first memento':
                self.mementos[link[1]] = link[2]
                self.first_memento = link[1] if link != None else None
            elif link[0] == 'last memento':
                self.mementos[link[1]] = link[2]
                self.last_memento = link[1] if link != None else None
            link = self.get_next_link()

    def get_next_link(self):
        uri = None
        datetime = None
        rel = None
        resource_type = None
        for token in self.__tokens:
            if token[0] == '<':
                uri = token[1:-1]
            elif token[:9] == 'datetime=':
                datetime = token[10:-1]
            elif token[:4] == 'rel=':
                rel = token[5:-1]
            elif token[:5] == 'type=':
                resource_type = token[6:-1]
            elif token[:6] == 'until=':
                datetime = token[7:-1]
            elif token == ';':
                None
            elif token == ',':
                return ( rel, dateutil.parser.parse(datetime)
                              if datetime != None else None,
                              uri, resource_type )
            else:
                raise Exception('Unexpected timemap token', token)
        if uri == None:
            return None
        else:
            return ( rel, dateutil.parser.parse(datetime)
                      if datetime != None else None,
                      uri, resource_type )

    def __getitem__(self, key):
        return self.mementos[key]

#==================================================================
class TimeMapTokenizer(object):
#==================================================================

    def __init__(self, uri=None, data=None):
        if uri is not None:
            self._tmfile = urllib2.urlopen(uri)
        elif data is not None:
            self._tmfile = StringIO.StringIO(data)
        self._tokens = []

    def __iter__(self):
        return self

    def next(self):
        if len(self._tokens) == 0:
            line = self._tmfile.readline()
            if len(line) == 0:
                raise StopIteration
            self._tokens = tokenizer.findall(line)
        return self._tokens.pop(0)

#===============================================================================
# MAIN FOR TESTING
#===============================================================================

if __name__ == "__main__":
	import logging
	logging.basicConfig()

	link_data_path = '/home/rachel/Desktop/CS_432/A2/test_doc.txt'
	memento_data = {}
	memento_file = open(link_data_path, "r")
	for line in memento_file:
		timemap_uri = 'http://mementoproxy.cs.odu.edu/aggr/timemap/link/1/' + line

		response = urllib.urlopen(timemap_uri)
		if response.getcode() == 200:
			tm = TimeMap(uri=timemap_uri);
			number_of_mementos = len(tm.mementos)
			memento_data[timemap_uri] = number_of_mementos
		else:
			memento_data[timemap_uri] = 0

	pprint(memento_data)
