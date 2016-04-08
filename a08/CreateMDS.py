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
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    blognames, words, data=clusters.readfile('blogdata.txt')
    coords, n_iterations = clusters.scaledown(data)
    clusters.draw2d(coords, blognames, jpeg='blogs2d.jpg')

    print("Number of iterations is %d" % n_iterations)

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    return

if __name__ == '__main__':
    main()
    sys.exit(0)