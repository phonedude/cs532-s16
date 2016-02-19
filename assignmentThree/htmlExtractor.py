#-*- coding: utf-8 -*-

import requests
#import uuid
import os


URIFile = open('uriFile.txt', 'r') #Opens the file w/ all of the uri's to test in read mode
outputFile = open('hashUnedited.txt', 'w')
counter = 0

ScriptPartOne = "echo -n '" 
ScriptPartTwo = "' | md5sum >> hashUnedited.txt"
ScriptPartThree = "lynx -source "
ScriptPartFour = " > "
ScriptPartFive = "lynx -dump -force_html "
ScriptPartSix = ".processed"

with open('uriFile.txt') as f: 
    lines = f.readlines()
    lines = [x.strip('\n') for x in lines]

for URLS in lines:
    r = os.system(ScriptPartOne + URLS + ScriptPartTwo)
    #outputFile.write(r.text())

HashFile = open('hashUnedited.txt', 'a')
with open('hashUnedited.txt') as z: 
    hashName = z.readlines()
    hashName = [x.strip('\n') for x in hashName]
    hashName = [n.strip(' *- ') for n in hashName]

HashFileNames = open('editedFileNames.txt', 'a')
for names in hashName: 
    a = os.system(ScriptPartThree + lines[counter] + ScriptPartFour + hashName[counter])
    HashFileNames.write(hashName[counter])
    HashFileNames.write("\n")	
    counter += 1
HashFileNames.close()
with open('editedFileNames.txt') as s: 
    readFiles = s.readlines()
    readFiles = [i.strip('\n') for i in readFiles]

for loop in readFiles:
    print loop
    q = os.system(ScriptPartFive + loop + ScriptPartFour + loop + ScriptPartSix)
    #outputFile.write(r.text())

URIFile.close() 
HashFile.close()