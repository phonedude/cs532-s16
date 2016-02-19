from math import *


f = open("tf.txt","r")
out = open ("out.csv","a")
i = 0
tf = []
URI = []
for i in range (1,21):
    if i % 2 == 0:
        URI.append(f.readline())
    else:
        tf.append(f.readline())

out.write("TFIDF,TF,IDF,URI\n")

for  x in range (0,10):
       
    TFIDF = float(tf[x]) * 10.3 
    out.write(str(TFIDF) + "," + str(tf[x]) + "," + str("10.3") + "," + str(URI[x]) + "\n")
