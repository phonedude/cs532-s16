import os
import sys
import json
from gender_detector import GenderDetector
from time import strftime, localtime, time


__author__ = 'Plinio H. Vargas'
__date__ = 'Sat,  Mar 12, 2016 at 16:51:56'
__email__ = 'pvargas@cs.odu.edu'


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# record running time
start = time()
print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
detector = GenderDetector('us')

with open("jose.json", 'rb') as file:
    data = json.load(file)

counter = 0
unknown = []
with open("jose-gender.data", 'w') as file:
    for name in data['nodes']:
        counter += 1
        try:
            print(counter, name['name'].split()[0].encode('ascii'), detector.guess(name['name'].split()[0]), name['id'])
            file.write('%s, %s, %s\n' % (str(name['id']), name['name'].split()[0].encode('ascii'), detector.guess(name['name'].split()[0])))
        except:
            print(counter, name['name'].split()[0], 'unknown')
            file.write('%s, %s, unknown\n' % (str(name['id']), name['name'].split()[0].encode('utf-8')))

print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
print('Execution Time: %.2f seconds' % (time()-start))
