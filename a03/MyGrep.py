import os
import re
import sys
from time import strftime, localtime, time
from collections import Counter

__author__ = 'Plinio H. Vargas'
__date__ = 'Sat,  Feb 13, 2016 at 16:55:36'
__email__ = 'pvargas@cs.odu.edu'


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

uri_linkfile = 'rankedURI'
raw_dir = 'URI-work-files/'

# record running time
start = time()
print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

# get processed resources
processed_files = [x for x in [x for x in os.walk(raw_dir)][0][2] if x[-10:] == '.processed']
for file in processed_files:
    with open(raw_dir + file, 'r', encoding='iso-8859-1') as p_file:
        words = re.findall('\w+', p_file.read().lower())
        cnt = Counter()
        for word in words:
            cnt[word] += 1

        print(file, sum(cnt.values()), cnt['football'])

print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
print('Execution Time: %.2f seconds' % (time()-start))