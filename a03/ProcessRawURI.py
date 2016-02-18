import os
import requests
import sys
from time import strftime, localtime, time
from subprocess import call
from hashlib import md5

__author__ = 'Plinio H. Vargas'
__date__ = 'Fri,  Feb 12, 2016 at 16:39:41'
__email__ = 'pvargas@cs.odu.edu'


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

uri_linkfile = '../a2/linkfiles.txt'
# uri_linkfile = 'rankedURI'
work_dir = 'URI-work-files/'
# work_dir = 'query-work-files/'
p_extension = '.processed'

# record running time
start = time()
print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

# get resources from sample URIs
counter = 0
with open(uri_linkfile, 'r') as file:
    for uri in file:
        counter += 1
        uri = uri.strip()
        r = requests.get(uri)
        print(r.text)

        # create hash for URI
        out = md5(uri.encode()).hexdigest()

        # save into working_directory
        with open(work_dir + out, 'w') as raw_file:
            raw_file.write(r.text)

        print(counter, uri, out)

# remove HTML markup from processed files in processed dir
raw_files = [x for x in os.walk(work_dir)][0][2]
for raw_file in raw_files:
    # place query-work-files-processed file into processed directory
    with open(work_dir + raw_file + p_extension, 'w') as file:
        call(["lynx", "-dump", "-force_html", work_dir + raw_file], stdout=file)



print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
print('Execution Time: %.2f seconds' % (time()-start))