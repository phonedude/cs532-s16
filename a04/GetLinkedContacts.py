import os
import sys
from time import strftime, localtime, time
import re
import requests

__author__ = 'Plinio H. Vargas'
__date__ = 'Tue,  Feb 23, 2016 at 21:36:14'
__email__ = 'pvargas@cs.odu.edu'


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from lib.WEBlib import AddURI

# record running time
start = time()
print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

with open('source.txt', 'r', encoding='iso-8859-1') as file:
    x = file.read()

counter = 0
followers_dict = {}
contact_link = set()
for link in re.findall("/view\?id=li_\d+\&amp;trk=contacts-contacts-list-contact_name-0", x):
    contact_link.add(link)

print(len(contact_link), contact_link)
contact_link = list(contact_link)
my_cookies = {'IN_HASH': 'state%3DDCEEFWF45453sdffef424', 'token': 'rO4kZEq6FkI8h24u9JXoMBhhVuQ%3D%7Cd0gwcW45KAXRoAiIy1ZmClIIA%2Ftw9j75G%2F3FQPq2zkX7%2ByDvaA2bUMnzLU%2B%2BfCHk8Ebag90MqnWPpmCerv25LJ%2FsFGFAR6Bi28Mjjwefx3GR1szE4sLgP%2BlfL0dNvHihbuGajwzDRUBmvRIDdvBzX8j%2BjKYtbObQuklA1KKFDC5eYmyKrqL42nkHhehnqoUh09u%2Blp%2BMhv%2BW7q7g9us1eMmhqtf2rExxcgaG%2FHJLwuuf7gzj9NoEZ0vwg9ffR2Y7bLqFK%2FyFZbc9Kg%2BPlDZDyw%3D%3D'}

s = requests.Session()
r = s.get('https://www.linkedin.com/contacts' + contact_link[0], cookies=my_cookies)
print(r.text)
my_list = set()
print('https://www.linkedin.com/contacts' + contact_link[0])

AddURI(my_list, 'https://www.linkedin.com/contacts' + contact_link[0])
print(my_list)
"""
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
"""

print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
print('Execution Time: %.2f seconds' % (time()-start))