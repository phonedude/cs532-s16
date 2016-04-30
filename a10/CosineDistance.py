import sys
import os
import math

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

title = []
def main():
    m = 500
    n = 100
    k = 0
    terms = []
    data = []

    with open('blogdata.txt') as file:
        for record in file:
            record = record.split()
            if k < 1:
                terms = record[-500:]
            else:
                print(k, len(record) - m, record[0:len(record) - m])
                title.append(record[0:len(record) - m])
                data.append({'input': tuple([int(x) for x in record[-500:]])})
            k += 1
    print(terms)

    for k in range(100):
        print('(%s, %d)' % (' '.join(title[k]), k), end=',')
    print()

    k_values = [1, 2, 5, 10, 20]
    print('Closest Blog to %s' % ' '.join(title[76]))
    for k in k_values:
        print('\nk=%d' % k)
        knnestimate(data, data[76]['input'], k)

    print()
    print('Closest Blog to %s' % ' '.join(title[68]))
    for k in k_values:
        print('\nk=%d' % k)
        knnestimate(data, data[68]['input'], k)


    return


def getdistances(data, vec1):
    distancelist = []

    # Loop over every item in the dataset
    for i in range(len(data)):
        vec2 = data[i]['input']

        # Add the distance and the index
        distancelist.append((cosine_distance(vec1, vec2),i))

    # Sort by distance
    distancelist.sort()

    return distancelist


def cosine_distance(v1, v2):
    d = 0.0
    for i in range(len(v1)):
        d += (v1[i] - v2[i])

    return 1 - math.cos(d)


def knnestimate(data, vec1, k=5):
    # Get sorted distances
    dlist = getdistances(data, vec1)
    avg = 0.0

    print(dlist)
    # Take the average of the top k results
    for i in range(1, k + 1):
        idx = dlist[i][1]
        print(' '.join(title[idx]))

    return avg


if __name__ == '__main__':
    main()
    sys.exit(0)
