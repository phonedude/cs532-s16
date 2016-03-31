__author__ = 'Plinio H. Vargas'
__date__ = 'Mar 29, 2016 01:55 AM'

import sys


def main():
    counter = 0
    with open('ml-100k/u.data', mode='rt', encoding='iso-8859-1') as file:
        for line in file:
            counter += 1
            record = line.split()
            for i in range(len(record) - 1):
                print(record[i], '\t', end='')
            print(record[len(record) - 1])
    return


if __name__ == '__main__':
    main()
    sys.exit(0)