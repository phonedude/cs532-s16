import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from StringIO import StringIO

edgeW = open("F:\Web_Science\cs532-s16\A5\Wedges.txt","a")
f = open("zachary2.txt","r")
g = nx.Graph()

d = np.genfromtxt(f, delimiter=' ')

for i in range(0,34):
    for j in range(0,34):
        if d[i][j]== 0:
            pass
        else:
            g.add_edge(i,j,weight=d[i][j])
esmall =[(u,v) for (u,v,d) in g.edges(data=True) if d['weight'] <=2.0]
emed =[(u,v) for (u,v,d) in g.edges(data=True) if d['weight'] <=4.0]
elarge =[(u,v) for (u,v,d) in g.edges(data=True) if d['weight'] >=5.0]
plt.figure(figsize=(8,8))
pos=nx.spring_layout(g)
nx.draw_networkx_nodes(g,pos,node_size=500)
nx.draw_networkx_edges(g,pos,edgelist=elarge,width=2,edge_color='r')
nx.draw_networkx_edges(g,pos,edgelist=emed,width=2,edge_color='g')
nx.draw_networkx_edges(g,pos,edgelist=esmall,width=2,edge_color='b')
labels={}
for i in range(0,34):
    labels[i] = i
nx.draw_networkx_labels(g,pos,labels,font_size=16)
plt.axis('off')
for line in nx.generate_edgelist(g):
    edgeW.write(line +'\n')
plt.savefig("F:\Web_Science\cs532-s16\A5\kEdges.png")
plt.show()
