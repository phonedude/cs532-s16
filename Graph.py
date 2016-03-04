#http://networkx.github.io/documentation/latest/examples/graph/karate_club.html
#Zachary's Karate Club graph
#Data file from:
#http://vlado.fmf.uni-lj.si/pub/networks/data/Ucinet/UciData.htm
import networkx as nx
import matplotlib.pyplot as plt

f=open("kNodes.txt","a")
G=nx.karate_club_graph()
plt.figure(figsize=(8,8))
nx.draw_networkx(G)
plt.axis('off')
f.write("Node Degree")
for v in G:
    f.write('%s     %s\n' % (v,G.degree(v)))
plt.savefig("kClubGraph.png")
plt.show()

