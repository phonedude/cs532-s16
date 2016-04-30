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

    outfile = open('k-clusters.txt', 'w')
    blognames, words, data=clusters.readfile('blogdata.txt')
    k_means = [5, 10, 20]
    for k in k_means:
        kclust, n_iterations = clusters.kcluster(data, k=k)

        counter = 0
        for i in range(len(kclust)):
            outfile.write('Cluster-%d:\n%s\n' % (i, ('-' * 9)))
            print('Cluster-%d:\n%s' % (i, ('-' * 9)))
            for r in kclust[i]:
                counter += 1
                outfile.write('%s,' % blognames[r])
                print(blognames[r], end=', ')
                if counter % 5 == 0:
                    outfile.write('\n')
                    print()
            outfile.write('\n')
            print('\n')

        outfile.write('Number of iterations for k=%d is %d.\n\n\n' % (k, n_iterations + 1))
        print('Number of iterations for k=%d is %d.\n\n\n' % (k, n_iterations + 1))

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    return

if __name__ == '__main__':
    main()
    sys.exit(0)