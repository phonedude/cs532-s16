import os
import sys
from time import strftime, localtime, time
import re
import operator

__author__ = 'Plinio H. Vargas'
__date__ = 'Thu,  Feb 25, 2016 at 07:47:42'
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
following_dict = {counter: 71}
for following in re.findall('\"friends_count\":\d+', x):
    counter += 1
    following_dict[counter] = int(re.findall('\d+', following)[0])
    print(counter, following, re.findall('\d+', following)[0])

print(sorted(following_dict.items(), key=operator.itemgetter(1)))
friend = 0
with open('twitter_paradox_2.dat', 'w') as file:
    file.write('Friend\tfollowing\n')
    for friend_tuple in sorted(following_dict.items(), key=operator.itemgetter(1)):
        friend += 1
        if friend_tuple[0] == 0:
            file.write('sis\t%d\n' % friend_tuple[1])
        else:
            file.write('f%d\t%d\n' % (friend, friend_tuple[1]))

print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
print('Execution Time: %.2f seconds' % (time()-start))