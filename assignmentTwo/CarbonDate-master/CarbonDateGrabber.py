#-*- coding: utf-8 -*-

import requests
#import uuid
import os
import datetime
from dateutil import parser


n = datetime.datetime.now()
empty_string = ""
date_format = "%Y-%m-%dT%H:%M:%S"
new_date_format = "%Y-%m-%d"
condensedFile = open('condensed.txt', 'r') #Opens the file w/ all of the uri's to test in read mode
counter = 0
age = 0

ScriptName = "python local.py"  #Using the provided momentoproxy

with open('condensed.txt') as f: #goes through the condensed file to grab all of the URI's
    lines = f.readlines()
    lines = [x.strip('\n') for x in lines]

for URLS in lines:
    r = os.system(ScriptName + ' http://' + URLS)
    print ScriptName + ' http://' + URLS
    #num_lines = sum(1 for line in open(str(unique_filename)))
    #NumbersFile.write(str(total)) #adds the total momentos for the single timemap to the NumbersFile 
    #NumbersFile.write("\n")
    #counter = counter + 1

AgeFile = open('URLAgeNumbers.txt', 'a')
FinalAgeFile = open('FinalAgeFile.txt', 'a')
with open('URLAgeNumbers.txt') as z: 
    Age = z.readlines()
    Age = [x.strip('\n') for x in Age]

for cAges in Age: 
    if cAges != empty_string:
        y = datetime.datetime.strptime(cAges, date_format)
        p = n.date() - y.date()
        a = str(p).split("days", 1)[0]
        FinalAgeFile.write(a)
        FinalAgeFile.write("\n")
    #print cAges


condensedFile.close()
AgeFile.close()
FinalAgeFile.close()