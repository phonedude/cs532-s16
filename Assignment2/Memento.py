from bs4 import BeautifulSoup
import requests
import urllib
f = open("F:\Web_Science\cs532-s16\Assignment2\links.txt", "r")
g= open("F:\Web_Science\cs532-s16\Assignment2\mems.txt", "a")
array = []
g.write("Number of Mementos")
for line in f:
    array.append(line)
for link in array:
    u = "http://mementoproxy.cs.odu.edu/aggr/timemap/link/1/%s"%link
    r = requests.head(u)
    if r.status_code in range(400,600):
        m=0
        g.write(str(m)+ "\n")
        #g.write(',')
    else:
        url = urllib.request.urlopen(u) 
        htmlPage = url.read()
        mem = str(htmlPage)
        m= mem.count('rel="memento"')
        g.write(str(m)+"\n")
        #g.write(',')
f.close