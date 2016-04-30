import os
import sys
from time import strftime, localtime, time
import re
import operator

__author__ = 'Plinio H. Vargas'
__date__ = 'Tue,  Feb 23, 2016 at 21:36:14'
__email__ = 'pvargas@cs.odu.edu'


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# record running time
start = time()
print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

with open('twitter', 'r', encoding='iso-8859-1') as file:
    x = file.read()

counter = 0
followers_dict = {}
for followers in re.findall('\"followers_count\":\d+', x):
    counter += 1
    followers_dict[counter] = int(re.findall('\d+', followers)[0])
    print(counter, followers, re.findall('\d+', followers)[0])
followers_dict[0] = counter

print(sorted(followers_dict.items(), key=operator.itemgetter(1)))
friend = 0
with open('twitter_paradox.dat', 'w') as file:
    file.write('Friend\tFollowers\n')
    for friend_tuple in sorted(followers_dict.items(), key=operator.itemgetter(1)):
        friend += 1
        if friend_tuple[0] == 0:
            file.write('sis\t%d\n' % friend_tuple[1])
        else:
            file.write('f%d\t%d\n' % (friend, friend_tuple[1]))

print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
print('Execution Time: %.2f seconds' % (time()-start))