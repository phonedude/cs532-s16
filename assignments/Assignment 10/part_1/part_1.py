import numpredict
import clusters

if __name__ == "__main__":

  blognames,words,data=clusters.readfile('blogdata.txt')
  
  print 'F-Measure' # in data[75]
  #print 'distance list: ' + str(numpredict.getdistances(data, blognames, data[75]))
  print 'k = 1 ' + str(numpredict.knnestimate(data, blognames, data[75], k = 1))
  print 'k = 2 ' + str(numpredict.knnestimate(data, blognames, data[75], k = 2))
  print 'k = 5 ' + str(numpredict.knnestimate(data, blognames, data[75], k = 5))
  print 'k = 10 ' + str(numpredict.knnestimate(data, blognames, data[75], k = 10))
  print 'k = 20 ' + str(numpredict.knnestimate(data, blognames, data[75], k = 20))

  print '\nWeb Science and Digital Libraries Research Group' # in data[7]
  #print 'distance list: ' + str(numpredict.getdistances(data, blognames, data[7]))
  print 'k = 1 ' + str(numpredict.knnestimate(data, blognames, data[7], k = 1))
  print 'k = 2 ' + str(numpredict.knnestimate(data, blognames, data[7], k = 2))
  print 'k = 5 ' + str(numpredict.knnestimate(data, blognames, data[7], k = 5))
  print 'k = 10 ' + str(numpredict.knnestimate(data, blognames, data[7], k = 10))
  print 'k = 20 ' + str(numpredict.knnestimate(data, blognames, data[7], k = 20))
