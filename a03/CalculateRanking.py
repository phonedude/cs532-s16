import os
import re
import math
import sys
from time import strftime, localtime, time
from collections import Counter
from hashlib import md5

__author__ = 'Plinio H. Vargas'
__date__ = 'Sat,  Feb 13, 2016 at 16:55:36'
__email__ = 'pvargas@cs.odu.edu'


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# record running time
start = time()
print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

# initialize working variables
term = 'football'
table_file = 'documents/table1.tex'
uri_linkfile = '../a2/linkfiles.txt'
uri_rankfile = 'rankedURI'
work_dir = 'URI-work-files/'
TF = 0                                                      # Term Frequency
docs_with_term = 1.29 * math.pow(10, 9)                     # docs with term
total_doc_corpus = 49.5 * math.pow(10, 9)                     # total docs in corpus
IDF = math.log(total_doc_corpus / docs_with_term, 2)
rank_tuples = []

"""
IDF(term) = log(total_doc_corpus / docs_with_term)
TF-IDF = TF * IDF
"""

hash_table = {}
for line in (open(uri_linkfile, 'r')):
    hash_table[md5(line.strip().encode()).hexdigest()] = line.strip()

# get processed resources
rank_files = [line.strip() for line in (open(uri_rankfile, 'r'))]
for file in rank_files:
    with open(work_dir + file.strip(), 'r', encoding='iso-8859-1') as p_file:
        words = re.findall('\w+', p_file.read().lower())
        cnt = Counter()
        for word in words:
            cnt[word] += 1

        TF = cnt[term] / sum(cnt.values())
        rank_tuples.append((file, sum(cnt.values()), cnt[term], TF, IDF, TF * IDF))

        #print('File:%s info: Words-in-file: %d, term-count: %d, TF: %.4f, IDF: %.4f, TF-IDF: %.4f' %
        #      (hash_table[file[:-10]], sum(cnt.values()), cnt[term], TF, IDF, TF * IDF))
print('\nTFIDF  TF     IDF    URI\n-----  --     ---    ---')
for row in sorted(rank_tuples, key=lambda tfidf: tfidf[5], reverse=True):
    print('%.3f  %.3f  %.3f  %s\\\\' % (row[5], row[3], IDF, hash_table[row[0][:-10]]))

rank = 1
with open(table_file, 'w') as outfile:
    outfile.write('%%%s\n' % ('-' * 60))
    outfile.write('%	Table 1\n')
    outfile.write('%%%s\n' % ('-' * 60))
    outfile.write('\\hspace*{-15mm}\n\\begin{table}[!htbp]\n\\small\n')
    outfile.write('\\caption{10 Hits for the term \\enquote{%s}, ranked by TFIDF} \label{tab:table1}\n' % term)
    outfile.write('\\begin{center}\n\\hspace*{-10mm}\n\\begin{tabular}{| c | c | c | c | l |}\\hline\n')
    outfile.write('RNK & TFIDF & TF & IDF & \multicolumn{1}{c |}{URI}\\\\\n\\hline\n')
    for row in sorted(rank_tuples, key=lambda tfidf: tfidf[5], reverse=True):
        outfile.write('%d & %.3f & %.3f & %.3f & \\tiny \\url{%s}\\\\\n' %
                      (rank, row[5], row[3], IDF, hash_table[row[0][:-10]]))
        rank += 1
    
    outfile.write('\\hline\n\\end{tabular}\n')
    outfile.write('\\caption*{\\scriptsize The column labeled RNK (ranking) has an invert relationship with TFIDF. ' +
                  'The lower the ranking, the higher is TFIDF. Similarly, the higher the TFIDF value the more ' +
                  'significant is the relationship of our term \\enquote{football} in comparison with other URIs in ' +
                  'the table.}\\n')
    outfile.write('\\end{center}\n\\end{table}')


print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
print('Execution Time: %.2f seconds' % (time()-start))