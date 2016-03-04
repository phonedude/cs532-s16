import networkx as nx

def gnewman(club,splitTo = 2):
    itteration = 0
    # ok so why do I check the number of connected components
    # for an undirected graph it is know that a connected component of an
    # an undirected graph is a subgraph in which any two vertices are connected to each other by paths
    # this is useful for this application since we are splitting a graph into two subgraphs
    # ie to mathematically represent the splitting of the club
    while nx.number_connected_components(club) < splitTo:
        # returns to us edges with the weights
        between = nx.edge_betweenness_centrality(club,normalized=False)
        # we want the edges with the highest edge betweenness centrality
        # there might be ties so just get the max betweenness
        m = max(between.values())
        # unpack the tuple returned to us by between.items ((u,v), maxBetweenScore)
        for (hU,hV),val in between.items():
            # check to see if m(max betweenness score) is equal to val
            # removes ties along the way
            if val == m:
                club.remove_edge(hU,hV)
                print("removed edge %s--%s with betweenness score of %f"%(hU,hV,m))
        itteration += 1

        print("-------------------------")
        # this print out can be uncommented it simply shows the same metric as described two different ways
        # print(nx.number_connected_components(club),len(list(nx.connected_component_subgraphs(club))))
    print("total iterations %d for splitting into %d"%(itteration,splitTo))

if __name__ == "__main__":

    for splitTo in range(2,6):
        #this is a weighted version of the graph from http://www.nexus.igraph.org/api/dataset_info?id=1&format=html
        karateClub = nx.read_graphml("karate.GraphML")
        # karateClub = nx.read_gml("nxKclub2.gml")
        # karateClub = nx.karate_club_graph()
        gnewman(karateClub,splitTo)
        print("______________________________\n")
        nx.write_dot(karateClub,"kc%d.dot"%splitTo)

