import psycopg2
import re
import math

def getwords(doc):
  splitter=re.compile('\\W*')
  # Split the words by non-alpha characters
  words=[s.lower() for s in splitter.split(doc) 
          if len(s)>2 and len(s)<20]
  
  # Return the unique set of words only
  return dict([(w,1) for w in words])

class classifier:
  def __init__(self,getfeatures,filename=None):
    # Counts of feature/category combinations
    self.fc={}
    # Counts of documents in each category
    self.cc={}
    self.getfeatures=getfeatures
    self.setdb("cs532_db")
    
  def setdb(self,dbfile):
    # connecting with database
    conn_string = "host='localhost' dbname='cs532_db' user='postgres' password='postgres'"
    self.conn = psycopg2.connect(conn_string)
    self.con = self.conn.cursor()
    self.con.execute('create table if not exists fc(feature VARCHAR, ' +
                                                   'category INT ,' +
                                                   'count INT);')
    self.con.execute('create table if not exists cc(category INT, count INT)')
    self.conn.commit()


  def incf(self,f,cat):
    count=self.fcount(f,cat)
    if count==0:
      self.con.execute("insert into fc values ('%s','%s',1)"
                       % (f, cat))
    else:
      self.con.execute(
        "update fc set count=%d where feature='%s' and category='%s'" 
        % (count+1,f,cat)) 
  
  def fcount(self,f,cat):
    try:
        self.con.execute("select count from fc where feature='%s' and category=%s" % (f, cat))
        res = self.con.fetchone()
    except AttributeError:
      res = None

    if res==None: return 0
    else: return float(res[0])

  def incc(self,cat):
    count=self.catcount(cat)
    if count==0:
      self.con.execute("insert into cc values (%s, 1)" % (cat))
    else:
      self.con.execute("update cc set count=%d where category = %s"
                       % (count+1, cat))

  def catcount(self, cat):
    try:
      self.con.execute("select count from cc where category=%s" % cat)
      res=self.con.fetchone()
    except AttributeError:
      res = None

    if res==None: return 0
    else: return float(res[0])

  def categories(self):
    self.con.execute('select category from cc')
    cur = self.con.fetchall()
    return [d[0] for d in cur]

  def totalcount(self):
    self.con.execute('select sum(count) from cc')
    res = self.con.fetchone();
    if res==None: return 0
    return res[0]


  def add_training_data(self, data):
    sql_text = "INSERT INTO training_tb (trn_id, words) VALUES "
    for k in range(len(data)):
      sql_text += ("(%d, '%s')," % ((k + 1), " ".join(data[k + 1])))
    idx = len(sql_text) - 1
    sql_text = sql_text[:idx] + ';'
    print(sql_text)

    self.con.execute(sql_text)
    self.conn.commit()


  def set_categories(self, file):
    with open(file, mode='r') as infile:
      for sql_text in infile:
        self.con.execute(sql_text)
    self.conn.commit()


  def train(self,item, cat):
    features=self.getfeatures(item)
    # Increment the count for every feature with this category
    for f in features:
      self.incf(f, cat)

    # Increment the count for this category
    self.incc(cat)
    self.conn.commit()

  def get_data(self, sql_text):
    self.con.execute(sql_text)

    return self.con.fetchall()


  def fprob(self,f,cat):
    if self.catcount(cat)==0: return 0

    # The total number of times this feature appeared in this 
    # category divided by the total number of items in this category
    #print('fprob=', self.fcount(f,cat)/self.catcount(cat), 'fcount=',
    #      self.fcount(f,cat), 'catcount=', self.catcount(cat))
    return self.fcount(f,cat)/self.catcount(cat)

  def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
    # Calculate current probability
    basicprob=prf(f,cat)

    # Count the number of times this feature has appeared in
    # all categories
    totals=sum([self.fcount(f,c) for c in self.categories()])

    # Calculate the weighted average
    bp=((weight*ap)+(totals*basicprob))/(weight+totals)
    return bp


class naivebayes(classifier):
  
  def __init__(self,getfeatures):
    classifier.__init__(self,getfeatures)
    self.thresholds={}
  
  def docprob(self,item,cat):
    features=self.getfeatures(item)   

    # Multiply the probabilities of all the features together
    p=1
    for f in features: p*=self.weightedprob(f, cat, self.fprob)
    return p

  def prob(self, item, cat):
    catprob = self.catcount(cat) / self.totalcount()
    docprob = self.docprob(item, cat)
    return docprob * catprob
  
  def setthreshold(self,cat,t):
    self.thresholds[cat]=t
    
  def getthreshold(self,cat):
    if cat not in self.thresholds: return 1.0
    return self.thresholds[cat]
  
  def classify(self,item,default=None):
    probs={}
    # Find the category with the highest probability
    max=0.0
    for cat in self.categories():
      probs[cat]=self.prob(item,cat)
      if probs[cat]>max: 
        max=probs[cat]
        best=cat

    # Make sure the probability exceeds threshold*next best
    for cat in probs:
      if cat==best: continue
      if probs[cat]*self.getthreshold(best)>probs[best]: return default
    return best

class fisherclassifier(classifier):
  def cprob(self,f,cat):
    # The frequency of this feature in this category    
    clf=self.fprob(f, cat)
    if clf==0: return 0

    # The frequency of this feature in all the categories
    freqsum=sum([self.fprob(f,c) for c in self.categories()])

    # The probability is the frequency in this category divided by
    # the overall frequency
    p=clf/(freqsum)
    
    return p


  def fisherprob(self,item,cat):
    # Multiply all the probabilities together
    p=1
    features=self.getfeatures(item)
    for f in features:
      p*=(self.weightedprob(f,cat,self.cprob))

    # Take the natural log and multiply by -2
    fscore=-2*math.log(p)

    # Use the inverse chi2 function to get a probability
    return self.invchi2(fscore,len(features)*2)


  def invchi2(self,chi, df):
    m = chi / 2.0
    sum = term = math.exp(-m)
    for i in range(1, df//2):
        term *= m / i
        sum += term
    return min(sum, 1.0)


  def __init__(self,getfeatures):
    classifier.__init__(self,getfeatures)
    self.minimums={}


  def setminimum(self,cat,min):
    self.minimums[cat]=min


  def getminimum(self,cat):
    if cat not in self.minimums: return 0
    return self.minimums[cat]


  def classify(self,item,default=None):
    # Loop through looking for the best result
    best=default
    max=0.0
    for c in self.categories():
      p=self.fisherprob(item,c)
      # Make sure it exceeds its minimum
      if p>self.getminimum(c) and p>max:
        best=c
        max=p
    return best


def sampletrain(cl):
  #cl.train('Nobody owns the water.','good')
  #cl.train('the quick rabbit jumps fences','good')
  #cl.train('buy pharmaceuticals now','bad')
  #cl.train('make quick money at the online casino','bad')
  #cl.train('the quick brown fox jumps','good')

  cl.train('Nobody owns the water.', 1)
  cl.train('the quick rabbit jumps fences', 1)
  cl.train('buy pharmaceuticals now',2)
  cl.train('make quick money at the online casino', 2)
  cl.train('the quick brown fox jumps', 1)
