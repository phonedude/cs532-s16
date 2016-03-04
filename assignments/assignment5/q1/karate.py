#! /usr/bin/env python

import pickle
import igraph
from igraph import *
import cairo

FILENAME = 'karate.pickle'
# load the graph
data = pickle.loads(open(FILENAME).read())['karate']

# Create faction list of actual group membership after split, 
# translated to values that would mirror a cut.membership list
factions_after_split = map(lambda x: int(x-1), data.vs['Faction'])

def compare(predicted):
	"""
	Compares the predicted and actual numerical lists and 
	returns a list of variant members and the accuracy of the prediction
	"""
	res = []
	for idx, val in enumerate(factions_after_split):
		if predicted[idx] != val:
			# Translate index to match original dataset
			res.append(idx + 1)
	return res, 100 - round(float(len(res)) / float(len(factions_after_split)) * 100, 2)

def print_results(method, res, acc):
	print("{} method results: \nVariant elements:\n\t{}\n{} % accuracy".format(method, res, acc))

if __name__ == '__main__':
	# Plot existing graph
	layout = data.layout('fr')
	plot(data, "initial_karate_graph.pdf", layout=layout, vertex_label=data.vs['name'], margin=30)

	# Girvan-Newman Edge Betweenness method
	com_eb = data.community_edge_betweenness(
		clusters=2, 
		directed=False, 
		weights=data.es['weight'])
        print(com_eb)
	clust_eb = com_eb.as_clustering()
        print(clust_eb)
	res_eb, acc_eb = compare(clust_eb.membership)
	plot(clust_eb, "clust_eb.pdf", vertex_label=data.vs['name'], margin=25)
	print_results("Edge Betweenness", res_eb, acc_eb)
		
	# Newman Leading Eigenvector method
	clust_le = data.community_leading_eigenvector(clusters=2, weights=data.es['weight'])
        print(clust_le)
	res_le, acc_le = compare(clust_le.membership)
	plot(clust_le, "clust_le.pdf", vertex_label=data.vs['name'], margin=25)
	print_results("Leading Eigenvector", res_le, acc_le)

	# Plot  3..5 community predictions
	for i in xrange(3, 6):
		cluster = data.community_edge_betweenness(
			clusters=i, 
			directed=False,
			weights=data.es['weight']).as_clustering()
                print (cluster)
		plot(cluster, "cluster" + str(i) + ".pdf", vertex_label=data.vs['name'], margin=25)