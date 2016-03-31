__author__ = 'Plinio H. Vargas'
__date__ = 'Mar 29, 2016 01:55 AM'

import sys


def main():
    counter = 0
    genre = []

    with open('ml-100k/u.item', mode='rt', encoding='iso-8859-1') as file:
        for line in file:
            record = line.split('|')
            for i in range(len(record) - 19):
                counter += 1
                if record[i] == 'unknown':
                    print(record[i], '\t01-Jan-1990\t ', '\t', end='')
                elif record[i].strip():
                    print(record[i].strip(), '\t', end='')
            if counter == 5 and not record[4].strip() and record[1] != 'unknown':
                print(' \t', end='')
            for i in range(len(record) - 19, len(record)):
                genre.append(int(record[i].strip()))

            print(tuple(genre), end='')
            counter = 0
            genre = []
            print()
    return


if __name__ == '__main__':
    main()
    sys.exit(0)