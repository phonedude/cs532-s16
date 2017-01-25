import igraph

g = igraph.Graph()

karate = igraph.Graph.Read_GraphML("karate.GraphML")

community_edge_betweenness(karate, clusters=2, directed=False)

print summary(karate)

# plot graph
igraph.plot(Karate)




