import sys
import os


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import a9.docclass as t


c1 = t.fisherclassifier(t.getwords)
#c1.train('the quick brown for jumps over the lazy dog', 'good')
#c1.train('make quick money in the online casino', 'bad')
#t.sampletrain(c1)
"""
for id, text, category in c1.get_data('select * from training_tb order by trn_id;'):
    if id < 51:
        print(id, text, category)
        c1.train(text, category)
"""
text = t.getwords('The Washington Wizards are 35-36 and if the season ended today would miss the playoffs. Here&#8217;s the Washington Post blog with a health update'.lower())
text = ' '.join([x for x in text])
print(c1.cprob(text, 7))
print(c1.cprob(text, 1))
print(1, c1.classify(text))
"""
print(1, c1.fisherprob(text, 1))
print(2, c1.fisherprob(text, 2))
print(3, c1.fisherprob(text, 3))
print(4, c1.fisherprob(text, 4))
print(5, c1.fisherprob(text, 5))
print(6, c1.fisherprob(text, 6))
print(7, c1.fisherprob(text, 7))
print(8, c1.fisherprob(text, 8))
#print(c1.cprob(''))
"""
c1.set_categories('categories.txt')
