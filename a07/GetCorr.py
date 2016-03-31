import os
import sys
import psycopg2
import operator
from time import strftime, localtime, time

__author__ = 'Plinio H. Vargas'
__date__ = 'Wed,  Mar 30, 2016 at 11:14:22'
__email__ = 'pvargas@cs.odu.edu'

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from lib.PCI_Code_Folder.chapter2.recommendations import *

def main():
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    # connecting with database
    conn_string = "host='localhost' dbname='cs532_db' user='postgres' password='postgres'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    # upload all users
    sql_text = "select user_id from user_tb;"
    cursor.execute(sql_text)
    all_users = cursor.fetchall()
    corr_table = {}

    # get my substitute me information
    my_sql = getSQL()
    my_index = 378
    substitute_me = getPrefs(cursor, my_sql(my_index))
    # print(substitute_me)

    # iterate through all users
    all_prefs = {}
    for person in all_users:
        other_index = person[0]
        other_person = getPrefs(cursor, my_sql(other_index))

        prefs = {other_index: other_person, my_index: substitute_me}
        all_prefs[other_index] = other_person

        # print(prefs)
        #print(other_index, sim_pearson(prefs, other_index, my_index))

        # build everyone preference
        corr_table[other_index] = sim_pearson(prefs, other_index, my_index)

    print('\nTop 5 most correlated substitute me')
    print('+%s+%s+' % ((10 * '-'), (16 * '-')))
    print('| {0:8} | {2:10} |'.format('Movie_id', 'Title'.rjust(20), 'Recomm Ranking'))
    print('+%s+%s+' % ((10 * '-'), (16 * '-')))
    most_corr = sorted(corr_table.items(), key=operator.itemgetter(1))[len(corr_table) - 6:-1]
    for correlation in sorted(most_corr, reverse=True, key=operator.itemgetter(1)):
        print('|{0:6d}    |     {1:.3f}      |'.format(correlation[0], correlation[1]))
    print('+%s+%s+' % ((10 * '-'), (16 * '-')))

    print('\n\nBottom 5 correlated substitute me')
    print('+%s+%s+' % ((10 * '-'), (16 * '-')))
    print('| {0:8} | {2:10} |'.format('Movie_id', 'Title'.rjust(20), 'Recomm Ranking'))
    print('+%s+%s+' % ((10 * '-'), (16 * '-')))
    least_corr = sorted(corr_table.items(), key=operator.itemgetter(1))[:5]
    for correlation in least_corr:
        print('|{0:6d}    |     {1:.3f}     |'.format(correlation[0], correlation[1]))
    print('+%s+%s+' % ((10 * '-'), (16 * '-')))

    recommendations = getRecommendations(all_prefs, my_index)
    # top recommendations of unseen movies
    print('\n\n             Substitute me 5 top unseen movies recommendations\n')
    print('+%s+%s+%s+' % ((10 * '-'),(51 * '-'), (16 * '-')))
    print('| {0:8} | {1:49} | {2:10} |'.format('Movie_id', 'Title'.rjust(20), 'Recomm Ranking'))
    print('+%s+%s+%s+' % ((10 * '-'),(51 * '-'), (16 * '-')))
    for a_top_recom in recommendations[:5]:
        # get movie title
        sql_text = "select title from movie_tb where movie_id = " + str(a_top_recom[1])
        cursor.execute(sql_text)
        title = cursor.fetchall()
        print('|{0:7d}   | {1:50}|     {2:.3f}      |'.format(a_top_recom[1], title[0][0], a_top_recom[0]))
    print('+%s+%s+%s+' % ((10 * '-'),(51 * '-'), (16 * '-')))

    # least recommendations of unseen movies
    size = len(recommendations) - 1
    print('\n\n\n            Substitute me 5 least unseen movies recommendations\n')
    print('+%s+%s+%s+' % ((10 * '-'),(51 * '-'), (16 * '-')))
    print('| {0:8} | {1:49} | {2:10} |'.format('Movie_id', 'Title'.rjust(20), 'Recomm Ranking'))
    print('+%s+%s+%s+' % ((10 * '-'),(51 * '-'), (16 * '-')))

    for i in range(5):
        # get movie title
        sql_text = "select title from movie_tb where movie_id = " + str(recommendations[size - i][1])
        cursor.execute(sql_text)
        title = cursor.fetchall()
        print('|{0:6d}    | {1:50}|     {2:.3f}      |'.format(recommendations[size - i][1], title[0][0],
                                                              recommendations[size - i][0]))
    print('+%s+%s+%s+' % ((10 * '-'),(51 * '-'), (16 * '-')))

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))


def getSQL():
    return lambda x: "select item_id, rating from rating_tb where user_id = " + str(x)

def getPrefs(p_cursor, sql_text):
    p_cursor.execute(sql_text)
    p_records = p_cursor.fetchall()

    person = {}

    for line in p_records:
        person[line[0]] = line[1]

    return person


if __name__ == '__main__':
    main()
    sys.exit(0)