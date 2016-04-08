import os
import sys
from time import strftime, localtime, time

__author__ = 'Plinio H. Vargas'
__date__ = 'Wed,  Mar 30, 2016 at 11:14:22'
__email__ = 'pvargas@cs.odu.edu'

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import lib.PCI_Code_Folder.chapter3.clusters as clusters

def main():
    blognames,words,data=clusters.readfile('blogdata.txt')
    clust=clusters.hcluster(data)
    outfile = open('ascii-dendogram.txt', 'w')
    clusters.printclust(clust, labels=blognames, file=outfile)
    outfile.close()
    clusters.drawdendrogram(clust,blognames,jpeg='blogclust.jpg')

    return

if __name__ == '__main__':
    main()
    sys.exit(0)