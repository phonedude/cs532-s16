import os
import sys
import re
import math
from time import strftime, localtime, time

__author__ = 'Plinio H. Vargas'
__date__ = 'Wed,  Mar 30, 2016 at 11:14:22'
__email__ = 'pvargas@cs.odu.edu'

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import lib.PCI_Code_Folder.chapter3.clusters as clusters

def main():

    n = 500
    m = 100
    matrix = []
    blognames = []
    matrix_total = [0] * n
    matrix_TDIF = [[0] * n for i in range(m)]
    total_doc_corpus = 0
    counter = 0
    with open('blogdata.txt', 'r') as infile:
        for line in infile:
            terms = line.strip().split('\t')
            if counter > 0:
                row = []
                row.append(terms[0])
                blognames.append(terms[0])
                i = 0
                for size in terms[1:]:
                    row.append(size)
                    matrix_total[i] += int(size)
                    total_doc_corpus += int(size)
                    i += 1
                matrix.append(row)
            counter += 1

    total_doc_corpus                     # total docs in corpus
    for i in range(m):
        for k in range(n):
            matrix_TDIF[i][k] = math.log(total_doc_corpus / matrix_total[k], 2) * int(matrix[i][k + 1])

    clust=clusters.hcluster(matrix_TDIF)
    outfile = open('ascii-dendogramP5.txt', 'w')
    clusters.printclust(clust, labels=blognames, file=outfile)
    outfile.close()
    clusters.drawdendrogram(clust,blognames,jpeg='blogclustP2.jpg')

    return

if __name__ == '__main__':
    main()
    sys.exit(0)