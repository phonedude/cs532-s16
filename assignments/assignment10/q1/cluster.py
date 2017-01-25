#! /usr/bin/python

import math

def cos_sim(v1, v2):
  sumxx, sumyy, sumxy = 0 ,0 ,0 
  for i in range(len(v1)):
    x = v1[i]; y = v2[i]
    sumxx += float(x)*float(x)
    sumyy += float(y)*float(y)
    sumxy += float(x)*float(y)
  return sumxy/math.sqrt(sumxx*sumyy)

def getdistances(data,vec1):
  distancelist=[]
  
  # Loop over every item in the dataset
  for i in range(len(data)):
    vec2=data[i]

    try:
      distancelist.append((cos_sim(vec1,vec2),i))
    except:
      pass
  
  # Sort by distance
  distancelist.sort()
  return distancelist

def knnestimate(data,vec1,k=5):
  # Get sorted distances
  dlist=getdistances(data,vec1)
  avg=0.0
  return dlist
vecs = {}

f = open("blogdata2.txt", "r")

for line in f:
	a = line.strip('\n').split('\t');
	b = a.pop(0)
	vecs[b] = a
	
print len(vecs)

fm = 'F-Measure'
ws = 'Web Science and Digital Libraries Research Group'

a = vecs[fm]
temp = vecs.values()
temp.pop(vecs.keys().index(fm))

a = knnestimate(temp,a,k=5)


k = [1, 2, 5, 10, 20]
print "------F-Measure kNN------"
for i in k:
  print "---k = "+str(i)
  for j in range(i):
    b = a[j][1]
    print vecs.keys()[b]

a = vecs[ws]
temp = vecs.values()
temp.pop(vecs.keys().index(ws))

a = knnestimate(temp,a,k=5)


k = [1, 2, 5, 10, 20]
print "-----WS-DL kNN-----"
for i in k:
  print "---k = "+str(i)
  for j in range(i):
    b = a[j][1]
    print vecs.keys()[b]    
