import local
import sys
import os
import subprocess




with open('urls.txt') as fil:
    for line in fil:
        #print line
        x= line
        subprocess.call("python local.py " + x, shell=True)
        
        
        
    	

