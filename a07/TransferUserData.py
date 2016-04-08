__author__ = 'Plinio H. Vargas'
__date__ = 'Mar 29, 2016 01:55 AM'

import sys


def main():
    with open('ml-100k/u.user', mode='rt', encoding='iso-8859-1') as file:
        for line in file:
            record = line.replace('|', '\t').strip()
            print(record)
    return


if __name__ == '__main__':
    main()
    sys.exit(0)