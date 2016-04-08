import re
import os
import sys
import requests
from time import strftime, localtime, time

__author__ = 'Plinio H. Vargas'
__date__ = 'Thu,  Feb 04, 2016 at 10:37:41'
__email__ = 'pvargas@cs.odu.edu'


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from lib.WEBlib import MementoCount

memento_uri = 'http://mementoproxy.cs.odu.edu/aggr/timemap/link/1/'
memento_date = strftime("mementodata/%Y%m%d.", localtime())
print(memento_date)

linknumber = 0
sample_size = 0
# iterates through all unique links to find and write to a file URI with mementos
with open('linkfiles.txt', 'r') as file:
    sample_size += 1
    for link in file:
        linknumber += 1
        uri = memento_uri + link.strip()
        r = requests.get(uri)
        if r.status_code == 200:
            mementofile = memento_date + str(linknumber)
            writefile = open(mementofile, 'w')
            writefile.write(r.text)
            writefile.close()
            print(len(re.findall(r'rel=\"memento\"', r.text)), link.strip(), r.status_code)

# create memento histogram data
# MementoCount(directory where files reside, outputfile, number of URIs)
MementoCount('mementodata', 'histogramdata', sample_size)