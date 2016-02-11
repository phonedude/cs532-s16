import os
import re
import sys
from time import strftime, localtime, time
from subprocess import call

__author__ = 'Plinio H. Vargas'
__date__ = 'Thu,  Feb 04, 2016 at 10:37:41'
__email__ = 'pvargas@cs.odu.edu'


PACKAGE_PARENT = '..'
CARBON_DATE_DIR = 'CarbonDate-master'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
sys.path.append(os.path.normpath(os.path.join(CARBON_DATE_DIR, PACKAGE_PARENT)))
print(SCRIPT_DIR)

from lib.WEBlib import Text2Json, GetURIage, GetNumberMementos

age_date = strftime("uriagedata/%Y%m%d.", localtime())
print(age_date)

linknumber = 0
# iterates through all unique links to find and write to a file URI with mementos
with open('linkfiles.txt', 'r') as file:
    os.chdir('../' + CARBON_DATE_DIR)
    for link in file:
        linknumber += 1
        filename = SCRIPT_DIR + '/' + age_date + str(linknumber)
        print(linknumber, filename)
        f = open(filename, "w")
        call(["python", "local.py", link.strip()], stdout=f)
        f.close()

counter_age = 0
counter_intercept = 0
# age URIs directory information
dir_info = [x for x in os.walk('uriagedata')]
filenames = dir_info[0][2]
dirpath = dir_info[0][0]

# memento directory information
dir_info = [x for x in os.walk('mementodata')]
mem_filenames = dir_info[0][2]
memento_path = dir_info[0][0]

with open('age-memeto-data.txt', 'w') as outfile:
    outfile.write('Age\tMementoQty\n')
    for filename in filenames:                              # for all files in memento directory
        with open(dirpath + '/' + filename, 'r') as file:   # open the file for reading
            for link in file:
                text = file.read()                          # place file content into text object
                age = GetURIage(Text2Json(text))            # get the age of link in days
                if age and age > -1:                        # if the link has an age
                    counter_age += 1                            # increase number of links with age values
                    link_number = filename.split('.')[1]        # find link e.i: 20160206.23   link=23

                    # for debugging
                    # print(link_number, age)

                    for match_file in mem_filenames:            # also find if link has mementos and get mementos qty
                        if re.search("[.]*\." + link_number + "$", match_file):
                            counter_intercept += 1
                            memento_qty = GetNumberMementos(memento_path + '/' + match_file)
                            print(link_number, age, memento_qty)
                            outfile.write('%d\t%d\n' %(age, memento_qty))
                            break


sample_size = len(filenames)
print("\n\nOut of %d URIs %d or %.2f%% have no estimated creation date." %
      (sample_size, sample_size - counter_age, (sample_size - counter_age) / sample_size * 100))

dir_info = [x for x in os.walk('a2/mementodata')]
no_mementos = sample_size - len(dir_info[0][2])
print("Out of %d URIs %d or %.2f%% have no mementos." %
      (sample_size, no_mementos, no_mementos / sample_size * 100))
print("Total mementos and age %d or %.2f%% where both variables intercept." %
      (counter_intercept, counter_intercept / sample_size * 100))