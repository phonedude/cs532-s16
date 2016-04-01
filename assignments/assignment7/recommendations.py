# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

import math
from math import sqrt
from numpy import mean
from operator import itemgetter
from pprint import pprint
from sys import stdout

# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs,person1,person2):
  # Get the list of shared_items
  si={}
  for item in prefs[person1]: 
	if item in prefs[person2]: si[item]=1

  # if they have no ratings in common, return 0
  if len(si)==0: return 0

  # Add up the squares of all the differences
  sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) 
					  for item in prefs[person1] if item in prefs[person2]])

  return 1/(1+sum_of_squares)

# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs, p1, p2):
	# Get the list of mutually rated items
	si={}
	for item in prefs[p1]: 
		if item in prefs[p2]: 
			si[item]=1

	# if they are no ratings in common, return 0
	if len(si)==0: return 0

	# Sum calculations
	n=len(si)

	# Sums of all the preferences
	sum1=sum([prefs[p1][it] for it in si])
	sum2=sum([prefs[p2][it] for it in si])

	# Sums of the squares
	sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
	sum2Sq=sum([pow(prefs[p2][it],2) for it in si])	

	# Sum of the products
	pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

	# Calculate r (Pearson score)
	num=pSum-(sum1*sum2/n)
	den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
	if den==0: return 0

	r=num/den
	filename = p1
	outfile = open(filename, 'a')	
	outfile.write(str(r) + "\t\t" + str(user1))
	outfile.write("\n")
	outfile.close()
	return r

# Returns the best matches for person from the prefs dictionary. 
# Number of results and similarity function are optional params.
def topMatches(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other) 
				  for other in prefs if other!=person]
  scores.sort()
  scores.reverse()
  return scores[0:n]

# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
  totals={}
  simSums={}
  for other in prefs:
	# don't compare me to myself
	if other==person: continue
	sim=similarity(prefs,person,other)

	# ignore scores of zero or lower
	if sim<=0: continue
	for item in prefs[other]:
		
	  # only score movies I haven't seen yet
	  if item not in prefs[person] or prefs[person][item]==0:
		# Similarity * Score
		totals.setdefault(item,0)
		totals[item]+=prefs[other][item]*sim
		# Sum of similarities
		simSums.setdefault(item,0)
		simSums[item]+=sim

  # Create the normalized list
  rankings=[(total/simSums[item],item) for item,total in totals.items()]

  # Return the sorted list
  rankings.sort()
  rankings.reverse()
  return rankings

def transformPrefs(prefs):
  result={}
  for person in prefs:
	for item in prefs[person]:
	  result.setdefault(item,{})
	  
	  # Flip item and person
	  result[item][person]=prefs[person][item] 
  return result

def calculateSimilarItems(prefs,n=10,similarity=sim_distance):
  # Create a dictionary of items showing which other items they
  # are most similar to.
  result={}
  # Invert the preference matrix to be item-centric
  itemPrefs=transformPrefs(prefs)
  c=0
  for item in itemPrefs:
	# Status updates for large datasets
	c+=1
	if c%100==0: print "%d / %d" % (c,len(itemPrefs))
	# Find the most similar items to this one
	scores=topMatches(itemPrefs,item,n=n,similarity=similarity)
	result[item]=scores
  return result

def calcSimilarUsers(prefs, n=10, similarity=sim_distance):
	result = {}
	itemPrefs = prefs
	c=0
	for item in itemPrefs:
		c+=1
		if c%100==0: print "%d / %d" % (c, len(itemPrefs))
		scores = topMatches(itemPrefs, item, n=n, similarity=similarity)
		result[item]=scores
	return result

def getRecommendedItems(prefs,itemMatch,user):
  userRatings=prefs[user]
  scores={}
  totalSim={}
  # Loop over items rated by this user
  for (item,rating) in userRatings.items( ):

	# Loop over items similar to this one
	for (similarity,item2) in itemMatch[item]:

	  # Ignore if this user has already rated this item
	  if item2 in userRatings: continue
	  # Weighted sum of rating times similarity
	  scores.setdefault(item2,0)
	  scores[item2]+=similarity*rating
	  # Sum of all the similarities
	  totalSim.setdefault(item2,0)
	  totalSim[item2]+=similarity

  # Divide each total score by total weighting to get an average
  rankings=[(score/totalSim[item],item) for item,score in scores.items( )]

  # Return the rankings from highest to lowest
  rankings.sort( )
  rankings.reverse( )
  return rankings

def loadMovieLens():
	# Get movie titles
	movies={}
	for line in open('u.item'):
		(id,title)=line.split('|')[0:2]
		movies[id]=title
	genre = {}
	for line in open('u.item'):
		(id, title, release, video, url, unknown, action, adventure, animation, childrens, comedy, crime, documentary, drama, fantasy, filmnoir, horror,musical, mystery, romance, scifi,  thriller, war, western)= line.split('|')[0:46]
		if int(action) == 1:
			genre[title]= 'action'
		elif int(adventure) == 1:
			genre[title]= 'adventure'
		elif int(animation) == 1:
			genre[title]= 'animation'
		elif int(childrens) == 1:
			genre[title]= 'childrens'
		elif int(comedy) == 1:
			genre[title]= 'comedy'
		elif int(crime) == 1:
			genre[title]= 'crime'
		elif int(documentary) == 1:
			genre[title]= 'documentary'
		elif int(drama) == 1:
			genre[title]= 'drama'
		elif int(fantasy) == 1:
			genre[title]= 'fantasy'
		elif int(filmnoir) == 1:
			genre[title]= 'filmnoir'
		elif int(horror) == 1:
			genre[title]= 'horror'
		elif int(musical) == 1:
			genre[title]= 'musical'
		elif int(romance) == 1:
			genre[title]= 'romance'
		elif int(thriller) == 1:
			genre[title]= 'thriller'
		elif int(scifi) == 1:
			genre[title]= 'scifi'
		elif int(western) == 1:
			genre[title]= 'western'
		elif int(war) == 1:
			genre[title]= 'war'
	# Load data
	prefs={}
	for line in open('u.data'):
		(user,movieid,rating,ts)=line.split('\t')
		prefs.setdefault(user,{})
		prefs[user][movies[movieid]]=float(rating)

	users={}
	for line in open('u.user'):
		(user, age, gender, job, zipcode) = line.split('|')
		users.setdefault(user, {})
		users[user] = {'age': age, 'gender': gender, 'job': job, 'zipcode': zipcode}
	
	mfavs = {}
	lfavs={}
	for line in open(r'u.item'):
		(id,title)= line.split('|')[0:2]
		if str(title) == 'Godfather, The (1972)':
			mfavs.setdefault(title)
		elif str(title) == 'Shawshank Redemption, The (1994)':
			lfavs.setdefault(title)
	return prefs, movies, genre, users, mfavs, lfavs

def get_avg(prefs, mid, user_filter=lambda x: True):
	ratings = []
	for user, user_ratings in prefs.iteritems():
		if user_filter(users[user]) and user_ratings.has_key(movies[mid]):
			ratings.append(user_ratings[movies[mid]])
	if not ratings:
		return 0.0
	return mean(ratings)


def get_top(sorted_list, key=lambda x, i: x[i][1], n=5):
	top = key(sorted_list, 0)
	top_items = []
	i = 0
	while i < n or key(sorted_list, i) == top:
		top_items.append(sorted_list[i])
		if i < n and key(sorted_list, i) != top:
			top = key(sorted_list, i)
		i += 1
	return top_items

def count_movie_ratings(prefs, mid, transform=False):
	num = 0
	for user, user_ratings in prefs.iteritems():
		if user_ratings.has_key(movies[mid]):
			num += 1
	return num

def get_sim_ratings(title, similar, top_key=lambda x, i: x[i][1], n=2000):
	itemPrefs = transformPrefs(prefs)
	matches = topMatches(itemPrefs, title, n=n, similarity=sim_pearson)
	sorted_m = sorted(matches, key=itemgetter(0), reverse=similar)
	return get_top(sorted_m, key=top_key, n=20)

def tabulate(tuples, caption, label, colnames, output):
	output.write('\\begin{table}[h!]\n')
	output.write('\\centering\n')
	opts = '| ' + ' | '.join(['l' for i in xrange(len(tuples[0]))]) + ' |'
	output.write('\\begin{{tabular}}{{{0}}}\n'.format(opts))
	output.write('\\hline\n')
	header = ' & '.join(['{}' for i in xrange(len(tuples[0]))]).format(*colnames)
	output.write(header + ' \\\\\n\\hline\n')
	for item in tuples:
		temp = ' & '.join(['{}' for i in xrange(len(item))])
		output.write(temp.format(*item) + ' \\\\\n')
	output.write('\\hline\n\\end{tabular}\n')
	output.write('\\caption{{{0}}}\n'.format(caption))
	output.write('\\label{{tab:{0}}}\n'.format(label))
	output.write('\\end{table}\n\n')	

def movies_not_rated(prefs, movies, userid, movie_type):
	userRatings = prefs[userid]
	count = 0
	movie_rated = {}
	for id, title in movies.items():
		temp = 0
		for item, rating  in userRatings.items():
			if title == item:
				temp = 1
				movie_rated.setdefault(title, rating)	
		for name, genre in movie_type.items():
			if title == name:
				if temp == 0:
					try:
						if genre == 'comedy':
							movie_rated[title] = '3.0'
							temp = 0
						elif genre == 'action':
							movie_rated[title] = '3.0'	
							temp = 0
						elif genre == 'crime':
							movie_rated[title] = '3.0'	
							temp = 0
						elif genre == 'drama':
							movie_rated[title] = '4.0'	
							temp = 0
						elif genre == 'thriller':
							movie_rated[title] = '5.0'	
							temp = 0
						elif genre == 'scifi':
							movie_rated[title] = '4.0'	
							temp = 0
						elif genre == 'war':
							movie_rated[title] = '3.0'	
							temp = 0
						elif genre == 'mystery':
							movie_rated[title] = '3.0'	
							temp = 0							
						else:
							movie_rated[title] = '1.0'	
							temp = 0
					except:
						pass
	return movie_rated
	
def pearson(avg1,avg2,prefs, movie1, movie2, movies):
	r={}
	r=0
	top = 0
	rbtm = 0
	lbtm = 0
	
	for user, movie in prefs.items():
		userRatings = prefs[user]
		for item, rating in userRatings.items():
			if movie1 == movies[item]:
				for user1, move in prefs.items():
					userRatings = prefs[user1]
					for item1, rating1 in userRatings.items():
						if movie2 == movies[item1]:
							if user1 == user:
								top += (rating-avg1)*(rating1-avg2)
								lbtm +=  (rating-avg1)*(rating-avg1)
								rbtm += (rating1-avg2)*(rating1-avg2)
	
	if lbtm == 0 or rbtm == 0:
		r = 5
		return r
	else:
		r = top/(math.sqrt(lbtm)* math.sqrt(rbtm))
	return r
	
print "Parsing data"
prefs, movies, genre, users, mfavs, lfavs = loadMovieLens()

def flatten(tup, f=lambda x: (x[0], x[1][0][1], x[1][0][0])):
	return f(tup)

if __name__ == '__main__': 
	with open('output.tex', 'w') as outfile:
		getuser = {}
		user_filter = lambda x: x['gender'] == 'M' and x['job'] == 'student' and int(x['age']) == 23
		ratings = []
		for mid, movie in movies.iteritems():
			for user, user_ratings in prefs.iteritems():
				if user_filter(users[user]) and user_ratings.has_key(movies[mid]):
					getuser.setdefault(int(user),{})
					getuser[int(user)][movies[mid]]=float(user_ratings[movies[mid]])
					ratings.append(user_ratings[movies[mid]])
		sorted_getuser = {}
		movie_sort = {}
		for user, user_movie in getuser.items():
			user_movie_sort = sorted(user_movie.items(), key=itemgetter(1), reverse=False)
			for title, rating in user_movie_sort[:3]:
				movie_sort.setdefault(title,rating)
			# print movie_sort
			sorted_getuser.setdefault(user, user_movie_sort[:3])
		sorted_avg_all = sorted(sorted_getuser.items(), key=itemgetter(0), reverse=False)
		# print sorted_avg_all
		top_raters = get_top(sorted_avg_all, key=lambda x,i: x[i][1][0])
		top_raters = [flatten(rater) for rater in sorted_avg_all]
		tabulate(top_raters, 'Users', 'user', ('User', 'Rating', 'Movie'), outfile)
		print "done with 1"
		most_correlated = {}
		least_correlated = {}
		for user, rest in users.iteritems():
			if int(user) == 135:
				for user1, rest in users.iteritems():
					if user == user1:
						pass
					else:
						r = sim_pearson(prefs, user, user1)
						if r == 1.0:
							most_correlated.setdefault(int(user1), r)
						if r == -1.0:
							least_correlated.setdefault(int(user1), r)
		sorted_most_correlated = sorted(most_correlated.items(), key=itemgetter(0), reverse=False)[len(most_correlated) - 6:-1]
		sorted_least_correlated = sorted(least_correlated.items(), key=itemgetter(0), reverse=False)[len(least_correlated) - 6:-1]
		tabulate(sorted_most_correlated, 'Most Correlated', 'most', ('User', 'Pearson\'s r'), outfile)
		tabulate(sorted_least_correlated, 'Least Correlated', 'least', ('User', 'Pearson\'s r'), outfile)
		print "done with 2"
		movie_rated1 = {}
		for user, rest in users.iteritems():
			if int(user) == 135:
				movie_rated1 = movies_not_rated(prefs, movies, user, genre)
		sorted_most_recomm = sorted(movie_rated1.items(), key=itemgetter(1), reverse=False)[len(movie_rated1) - 6:-1]
		sorted_least_recomm = sorted(movie_rated1.items(), key=itemgetter(1), reverse=True)[len(movie_rated1) - 6:-1]
		tabulate(sorted_most_recomm, 'Top 5 unseen movies recommendations', 'recommtop', ('Title', 'Recomm Ranking'), outfile)
		tabulate(sorted_least_recomm, 'Least 5 unseen movies recommendations', 'recommleast', ('Title', 'Recomm Ranking'), outfile)
		print "done with 3"
		fav_cor = {}
		nfav_cor ={}
		avg1 = get_avg(prefs, mfavs)
		for id, title in movies.items():
			avg2 = get_avg(prefs, id)
			r = pearson(avg1, avg2, prefs, mfavs, title)
			if r == 1.0:
				fav_cor.setdefault(str(title), str(r))
			elif r == -1.0:
				nfav_cor.setdefault(str(title), str(r))
		sorted_fav_correlated = sorted(fav_cor.items(), key=itemgetter(0), reverse=False)[len(fav_cor) - 6:-1]
		sorted_nfav_correlated = sorted(nfav_cor.items(), key=itemgetter(0), reverse=False)[len(nfav_cor) - 6:-1]
		tabulate(sorted_fav_correlated, 'Most Favourite Movie \textcolor{blue}{Godfather, The (1972)} Correlated', 'fav', ('Title', 'Pearson\'s r'), outfile)
		tabulate(sorted_nfav_correlated, 'Least Favourite Movie \textcolor{blue}{Godfather, The (1972)} Correlated', 'nfav', ('Title', 'Pearson\'s r'), outfile)
		print "done with 4"