import os
import sys
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from time import strftime, localtime, time


__author__ = 'Plinio H. Vargas'
__date__ = 'Thu,  Mar 2, 2016 at 14:07:32'
__email__ = 'pvargas@cs.odu.edu'


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# record running time
start = time()
print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

G = nx.karate_club_graph()

plt.figure(figsize=(8,8))

pos=nx.spring_layout(G) # positions for all nodes

nx.draw(G, pos, with_labels=True, node_size=500)
plt.savefig('documents/images/original-club.png')

nx.draw_networkx_nodes(G,pos,
                       nodelist=[0, 33],
                       with_labels=True,
                       node_color='y',
                       node_size=500)

plt.savefig('documents/images/original-sink-soruce.png')
plt.show()

print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
print('Execution Time: %.2f seconds' % (time()-start))
