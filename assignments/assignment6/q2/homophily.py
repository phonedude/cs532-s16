import os
import sys
import json

gender = {'female': 0, 'male': 0}
node_gender = {}
number_cross_gender  = 0

with open("9ulovesu-gender.json", 'r') as file:
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