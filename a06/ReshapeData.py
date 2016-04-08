import os
import sys
import json
import re
from time import strftime, localtime, time


__author__ = 'Plinio H. Vargas'
__date__ = 'Thu,  Mar 10, 2016 at 06:03:55'
__email__ = 'pvargas@cs.odu.edu'


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# record running time
start = time()
print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

colors = ['#ff9900', '#e69419', '#cc8f33', '#b98b46', '#9f8660']

with open("jose.data", 'r') as file:
    data = json.load(file)

print('{\n\t"nodes": [\n', end='')
cross_idx = {}
counter = 0
for record in data:
    cross_idx[record] = counter
    print('\t\t{\n\t\t\t"id": %s,\n\t\t\t"name": %s,\n\t\t\t"followers_count": %s,\n\t\t\t"friends_count": %s,\n\t\t\t'
          '"screen_name": %s,\n\t\t\t"avatar": %s,\n\t\t},\n' %
          (record, data[record]['name'], data[record]['followers_count'], data[record]['friends_count'],
           data[record]['screen_name'], data[record]['avatar']), end='')
    counter += 1
print('\t],\n\n\t"connections": [\n', end='')

print(cross_idx)

for record in data:
    for link in data[record]['connected_to']:
        if str(link) in cross_idx:
            print('\t\t{"source": %s, "target": %s, "type": "followed-by"},\n' % (cross_idx[str(record)], cross_idx[str(link)]), end='')
print('\t]\n}', end='')
network_size = counter

"""
Write to file
"""
outputfile = 'jose.json'
with open(outputfile, 'w') as file:
    file.write('{\n\t"nodes": [\n')
    for record in data:
        friendship = len(data[record]['connected_to']) / network_size
        if friendship > 0.20:
            friend_color = colors[0]
        elif friendship > 0.14:
            friend_color = colors[1]
        elif friendship > 0.10:
            friend_color = colors[2]
        elif friendship > 0.04:
            friend_color = colors[3]
        else:
            friend_color = colors[4]

        print(friendship)
        file.write('\t\t{\n\t\t\t"id": "%s",\n\t\t\t"name": "%s",\n\t\t\t"followers_count": "%s",'
                   '\n\t\t\t"friends_count": "%s",\n\t\t\t"screen_name": "%s",\n\t\t\t"avatar": "%s",'
                   '\n\t\t\t"color": "%s"\n\t\t},\n' %
              (record, data[record]['name'], data[record]['followers_count'], data[record]['friends_count'],
               data[record]['screen_name'], data[record]['avatar'], friend_color))
    file.write('\t],\n\n\t"links": [\n')

    for record in data:
        for link in data[record]['connected_to']:
            if str(link) in cross_idx:
#                file.write('\t\t{"source": %s, "target": %s, "type": "followed-by", "value": %d},\n' %
#                           (cross_idx[str(record)], cross_idx[str(link)], 1))
                file.write('\t\t{"source": %s, "target": %s, "type": "followed-by", "value": %d},\n' %
                           (str(record), str(link), 1))
    file.write('\t]\n}')

# remove extra commas
with open(outputfile, 'r+') as file:
    data = file.read()
    file.seek(0)
    file.write(re.sub('\},\n\t\]', '}\n\t]', data))
    file.truncate()

print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
print('Execution Time: %.2f seconds' % (time()-start))
