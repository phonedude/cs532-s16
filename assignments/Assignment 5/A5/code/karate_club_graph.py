import matplotlib
import networkx as nx
from matplotlib import pyplot as plt
import re

def girvan_newman(G):
	if len(G.nodes()) == 1:
		return [G.nodes()]
	def find_best_edge(G0):
		eb = nx.edge_betweenness_centrality(G0)
		eb_il = eb.items()
		eb_il.sort(key=lambda x: x[1], reverse=True)
		return eb_il[0][0]
	components = nx.connected_component_subgraphs(G)
	while len(list(components)) == 1:
		G.remove_edge(*find_best_edge(G))
		components = nx.connected_component_subgraphs(G)
	result = [c.nodes() for c in components]
	for c in components:
		result.extend(girvan_newman(c))
	return result

#with open('weighted_karate.gml') as f:
#		data = f.read()
#		data = map(int, re.findall('\d+', data))
#		print data

G=nx.karate_club_graph()
fig = plt.figure(figsize=(20,20))
nx.draw_networkx(G)
axis = plt.axis('off')
#plt.savefig('networkx_karate.png')
#print("Node Degree")
#for v in G:
#	print('%s %s' % (v,G.degree(v)))
gn = girvan_newman(G)
fig = plt.figure(figsize=(20,20))
nx.draw_networkx(gn)
axis = plt.axis('off')
#plt.savefig('girvan_newman.png')