import os
import sys
import json
import re
from time import strftime, localtime, time


__author__ = 'Plinio H. Vargas'
__date__ = 'Sat,  Mar 12, 2016 at 18:54:21'
__email__ = 'pvargas@cs.odu.edu'


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# record running time
start = time()
print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

counter = 0
gender_nodes = {}
with open("jose-gender.data", 'r') as file:
    for line in file:
        record = line.strip().split(',')
        if record[2].strip() == 'male' or record[2].strip() == 'female':
            counter += 1
            print(counter, record[0], record[1], record[2])
            gender_nodes[record[0]] = record[2].strip()
        else:
            print('error ->', repr(record[2]))

print(len(gender_nodes), gender_nodes)

print('{\n\t"nodes": [\n', end='')
counter = 0

with open("jose.json", 'r') as file:
    data = json.load(file)

for idx in gender_nodes:
    for node in data['nodes']:
        if idx == node['id']:
            print('\t\t{\n\t\t\t"id": %s,\n\t\t\t"name": %s,\n\t\t\t"followers_count": %s,\n\t\t\t'
                  '"friends_count": %s,\n\t\t\t"screen_name": %s,\n\t\t\t'
                  '"avatar": %s,\n\t\t\t"gender": %s\n\t\t},\n' %
                  (idx, node['name'], node['followers_count'], node['friends_count'],
                   node['screen_name'], node['avatar'], gender_nodes[idx]), end='')

print('\t],\n\n\t"links": [\n', end='')

counter = 0
linked_nodes = set()
for node in data['links']:
    if str(node['target']) in gender_nodes and str(node['source']) in gender_nodes:
        if (node['source'], node['target']) not in linked_nodes and (node['target'], node['source']) not in linked_nodes:
            counter += 1
            print('\t\t{"source": %s, "target": %s, "type": "followed-by"},\n' %
                  (node['source'], node['target']), end='')
            linked_nodes.add((node['source'], node['target']))
print('\t]\n}', end='')

print(len(linked_nodes), linked_nodes)
"""
   Write File
"""
outputfile = 'jose-gender.json'
with open(outputfile, 'w') as file:
    file.write('{\n\t"nodes": [\n')
    for idx in gender_nodes:
        for node in data['nodes']:
            if idx == node['id']:
                file.write('\t\t{\n\t\t\t"id": %s,\n\t\t\t"name": "%s",\n\t\t\t"followers_count": %s,\n\t\t\t'
                           '"friends_count": %s,\n\t\t\t"screen_name": "%s",\n\t\t\t'
                           '"avatar": "%s",\n\t\t\t"gender": "%s"\n\t\t},\n' %
                           (idx, node['name'], node['followers_count'], node['friends_count'],
                            node['screen_name'], node['avatar'], gender_nodes[idx]))

    file.write('\t],\n\n\t"links": [\n')

    linked_nodes = set()
    for node in data['links']:
        if str(node['target']) in gender_nodes and str(node['source']) in gender_nodes:
            if (node['source'], node['target']) not in linked_nodes and (node['target'], node['source']) not in linked_nodes:
                file.write('\t\t{"source": %s, "target": %s, "type": "followed-by"},\n' %
                           (node['source'], node['target']))
                linked_nodes.add((node['source'], node['target']))
    file.write('\t]\n}')

# remove extra commas
with open(outputfile, 'r+') as file:
    data = file.read()
    file.seek(0)
    file.write(re.sub('\},\n\t\]', '}\n\t]', data))
    file.truncate()

print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
print('Execution Time: %.2f seconds' % (time()-start))
