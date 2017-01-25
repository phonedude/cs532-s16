#-*- coding: utf-8 -*-

import requests
#import uuid
import os

condensedFile = open('condensed.txt', 'r') #Opens the file w/ all of the uri's to test in read mode
NumbersFile = open('TimeMapNumbers.txt', 'w')
counter = 0
lineNums = 0

URI = "http://mementoproxy.cs.odu.edu/aggr/timemap/link/1/"  #Using the provided momentoproxy

with open('condensed.txt') as f: #goes through the condensed file to grab all of the URI's
    lines = f.readlines()
    lines = [x.strip('\n') for x in lines]

for URLS in lines:
    r = requests.get(URI + 'http://' + URLS)
    print URI + 'http://' + URLS
    print r.status_code
    if r.status_code == 200:
        total = 0
        unique_filename = "TimeMaps/" + "x" + str(counter) 
        placeholder = open(unique_filename, 'w')  #opens up the dynamically created file
        placeholder.write(r.text)
        #num_lines = sum(1 for line in open(str(unique_filename)))
        placeholder.close()
        with open(str(unique_filename)) as fileLines: #grabs the amount of momentos from the file 
            for lineNums in fileLines:
                found = lineNums.find('archive')
                if found != -1 and found != 0:
                    total += 1
        print total
        NumbersFile.write(str(total)) #adds the total momentos for the single timemap to the NumbersFile 
        NumbersFile.write("\n")
        counter = counter + 1


condensedFile.close()
NumbersFile.close()