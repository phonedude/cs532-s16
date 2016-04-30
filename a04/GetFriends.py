import os
import sys
import operator
from time import strftime, localtime, time
import xml.etree.ElementTree as Tree

__author__ = 'Plinio H. Vargas'
__date__ = 'Sat,  Feb 20, 2016 at 19:09:22'
__email__ = 'pvargas@cs.odu.edu'


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# record running time
start = time()
print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

tree = Tree.parse('mln.graphml')
root = tree.getroot()
ns = {'structure': 'http://graphml.graphdrawing.org/xmlns'}
my_friends = root[len(root) - 1].findall('structure:node', ns)
friend = 0
friend_dict = {0: len(my_friends)}
for child in my_friends:
    friend += 1
    for element in child.findall('structure:data', ns):
        if element.attrib['key'] == 'friend_count':
            friend_dict[friend] = int(element.text)

print('Total Friends: %d, Missing Data: %d' % (len(my_friends), len(my_friends) - len(friend_dict)))
print(sorted(friend_dict.items(), key=operator.itemgetter(1)))
friend = 0
with open('ffriendship_paradox.dat', 'w') as file:
    file.write('Friend\tNo.Friends\n')
    for friend_tuple in sorted(friend_dict.items(), key=operator.itemgetter(1)):
        friend += 1
        if friend_tuple[0] == 0:
            file.write('mln\t%d\n' % friend_tuple[1])
        else:
            file.write('f%d\t%d\n' % (friend, friend_tuple[1]))


print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
print('Execution Time: %.2f seconds' % (time()-start))