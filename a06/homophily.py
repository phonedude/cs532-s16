import os
import sys
import json
from time import strftime, localtime, time


__author__ = 'Plinio H. Vargas'
__date__ = 'Wed,  Mar 16, 2016 at 20:06:10'
__email__ = 'pvargas@cs.odu.edu'


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# record running time
start = time()
print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

gender = {'female': 0, 'male': 0}
node_gender = {}
number_cross_gender  = 0

with open("jose-gender.json", 'r') as file:
    data = json.load(file)

for node in data['nodes']:
    node_gender[node['id']] = {'gender': node['gender'], 'name': node['name']}
    if node['gender'] == 'female':
        gender['female'] += 1
    elif node['gender'] == 'male':
        gender['male'] += 1

n = gender['male'] + gender['female']
p = gender['male'] / n
q = gender['female'] / n

print('\nNumber of females: %d' % gender['female'])
print('Number of males: %d' % gender['male'])
print('p: %.3f' % p)
print('q: %.3f' % q)
print('2pq: %.3f' % (2 * p * q))

print('\nCross-gender edges:\n%s\n' %(18 * '-'))
for links in data['links']:
    if node_gender[links['target']]['gender'] != node_gender[links['source']]['gender']:
        print('%s <--> %s' % (node_gender[links['target']]['name'], node_gender[links['source']]['name']))
        number_cross_gender += 1

print('\nSummary of Cross-gender edges: %d out of %d' % (number_cross_gender, len(data['links'])))
print('Percentage of Cross-gender edges %.3f' % (number_cross_gender / len(data['links'])))

print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
print('Execution Time: %.2f seconds' % (time()-start))
