import collections
import json

followers = collections.OrderedDict()
followers['AtHeartEngineer'] = []
with open('tylers_followers.txt') as f:
	for i, line in enumerate(f):
		line = line.strip()
		followers[line] = []
		followers['AtHeartEngineer'].append(line)
		# node_ids[line] = i + 1

node_ids = {}
for i, follower in enumerate(followers):
	node_ids[follower] = i
#print (followers)
source_target_pairs = []
current_pair = []
i = 0
with open('relationships.txt') as f:
	for line in f:
		if not line.startswith("#") and not line.strip() == '':
			i += 1
			current_pair.append(line)
			if (i % 2 == 0):
				source_target_pairs.append(current_pair)
				current_pair = []

for source_target in source_target_pairs:
	source_split = source_target[0].split()
	target_split = source_target[1].split()
	source_user = source_split[1].strip()
	target_user = target_split[1].strip()
	if source_split[0] == 'True':
		if source_user not in followers[target_user]:
			followers[target_user].append(source_user)
	if target_split[0] == 'True':
		if target_user not in followers[source_user]:
			followers[source_user].append(target_user)

d3_json = {"nodes": [], "links": []}
for follower in followers:
	# print ('follower', follower)
	d3_json['nodes'].append({'name':follower})
	source = node_ids[follower]
	for t in followers[follower]:
		target = node_ids[t]
		d3_json['links'].append({'source': source, 'target': target})
#print (json.dumps(followers, indent=4, sort_keys=True))
#print ('\n\n')
#print (json.dumps(d3_json, indent=4, sort_keys=False))

# Part 2

genders = None

with open("genders.json") as f:
	genders = json.load(f)

p = 0
q = 0
for person in genders:
	if genders[person] == "male":
		p += 1
	elif genders[person] == "female":
		q += 1

p /= len(genders)
q /= len(genders)
print ("p = " , p)
print ("q = " , q)
threshold = 2*p*q
print ("2pq = " , threshold)
edges = d3_json['links']
nodes = d3_json['nodes']
edge_count = 0
heterogeneous_count = 0
for edge in edges:
	source_number = edge['source']
	target_number = edge['target']
	source_username = nodes[source_number]['name']
	target_username = nodes[target_number]['name']
	if source_username in genders and target_username in genders:
		source_gender = genders[source_username]
		target_gender = genders[target_username]
		edge_count += 1
		if source_gender != target_gender and source_gender is not None and target_gender is not None:
			heterogeneous_count += 1

#print (edge_count)
#print (heterogeneous_count)
ratio = heterogeneous_count / edge_count
print ("ratio = " , ratio)