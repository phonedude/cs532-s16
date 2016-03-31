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
		movies[id]=title
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
	return prefs, movies, genre, users

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
print "Parsing data"

def movies_not_rated(prefs, movies, userid, movie_type):
	userRatings = prefs[userid]
	count = 0
	num = 0
	
	for id, title in movies.items():
		temp = 0
		for item,rating  in userRatings.items():
			if title == item:
				temp = 1
				filename = r"AllRated.txt"
				outfile = open(filename, 'a')
				outfile.write(str(title) +" "+str(rating))
				outfile.write("\n")
				outfile.close()	
		for name, genre in movie_type.items():
			if title == name:
				if temp == 0:
					try:
						if genre == 'comedy':
							filename = r"AllRated.txt"
							outfile = open(filename, 'a')
							outfile.write(str(title) +" 2.0")
							outfile.write("\n")
							outfile.close()	
							temp = 0
						elif genre == 'action':
							filename = r"AllRated.txt"
							outfile = open(filename, 'a')
							outfile.write(str(title) +" 1.0")
							outfile.write("\n")
							outfile.close()	
							temp = 0
						elif genre == 'crime':
							filename = r"AllRated.txt"
							outfile = open(filename, 'a')
							outfile.write(str(title) +" 4.0")
							outfile.write("\n")
							outfile.close()	
							temp = 0
						elif genre == 'drama':
							filename = r"AllRated.txt"
							outfile = open(filename, 'a')
							outfile.write(str(title) +" 5.0")
							outfile.write("\n")
							outfile.close()	
							temp = 0
						else:
							filename = r"AllRated.txt"
							outfile = open(filename, 'a')
							outfile.write(str(title) +" 3.0")
							outfile.write("\n")
							outfile.close()	
							temp = 0
					except:
						pass
	
	print(len(movies))
	
def movie_type_notrated(prefs, movie_type, user):
	userRatings = prefs[user]
	action1 = 0
	adventure1 = 0
	animation1 = 0
	comedy1 = 0
	crime1 = 0
	drama1 = 0
	fantasy1 = 0
	mystery1 = 0
	thriller1 = 0
	scifi1 = 0
	western1 = 0
	war1 = 0
	
	action2 = 0
	adventure2 = 0
	animation2 = 0
	comedy2 = 0
	crime2 = 0
	drama2 = 0
	fantasy2 = 0
	mystery2 = 0
	thriller2 = 0
	scifi2 = 0
	western2 = 0
	war2 = 0
	for id, name in movie_type.items():
		for item, rating in userRatings.items():
			if id == item:
				if rating == 5.0 and rating == 4.0:
					if name == 'action':
						action1+=1
					if name == 'adventure':
						adventure1+=1
					if name== 'animation':
						animation1+=1
					if name== 'comedy':
						comedy1+=1
					if name== 'crime':
						crime1+=1
					if name== 'drama':
						drama1+=1
					if name == 'fantasy':
						fantasy1+=1
					if name == 'mystery':
						mystery1+=1
					if name== 'thriller':
						thriller1+=1
					if name == 'scifi':
						scifi1+=1
					if name == 'western':
						western1+=1
					if name == 'war':
						war1+=1
				if rating <= 2.0:
					if name == 'action':
						action2+=1
					if name == 'adventure':
						adventure2+=1
					if name== 'animation':
						animation2+=1
					if name== 'comedy':
						comedy2+=1
					if name== 'crime':
						crime2+=1
					if name== 'drama':
						drama2+=1
					if name == 'fantasy':
						fantasy2+=1
					if name == 'mystery':
						mystery2+=1
					if name== 'thriller':
						thriller2+=1
					if name == 'scifi':
						scifi2+=1
					if name == 'western':
						western2+=1
					if name == 'war':
						war2+=1
			
	filename = r"favmovietypes.txt"
	outfile = open(filename, 'a')
	outfile.write("action " +str(action1) +" adventure"+str(adventure1))
	outfile.write("\n")
	outfile.write("animation " +str(animation1) +" comedy"+str(comedy1))
	outfile.write("\n")
	outfile.write("crime " +str(crime1) +" drama"+str(drama1))
	outfile.write("\n")
	outfile.write("fantasy " +str(fantasy1) +" mystery"+str(mystery1))
	outfile.write("\n")
	outfile.write("thriller " +str(thriller1) +" scifi"+str(scifi1))
	outfile.write("\n")
	outfile.write("war " +str(war1) +" western"+str(western1))
	outfile.write("\n")
	outfile.write("action " +str(action2) +" adventure"+str(adventure2))
	outfile.write("\n")
	outfile.write("animation " +str(animation2) +" comedy"+str(comedy2))
	outfile.write("\n")
	outfile.write("crime " +str(crime2) +" drama"+str(drama2))
	outfile.write("\n")
	outfile.write("fantasy " +str(fantasy2) +" mystery"+str(mystery2))
	outfile.write("\n")
	outfile.write("thriller " +str(thriller2) +" scifi"+str(scifi2))
	outfile.write("\n")
	outfile.write("war " +str(war2) +" western"+str(western2))
	outfile.write("\n")
	outfile.close()
	

prefs, movies, genre, users = loadMovieLens()
movie_type_notrated(prefs, genre, '135')

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
		for user, rest in users.iteritems():
			if int(user) == 135:
				movies_not_rated(prefs, movies, user, genre)
	# my_user = 135
	# for user, user_ratings in prefs.iteritems():
		# recommendations = getRecommendations(user, my_user)
		# for top_recom in recommendations[:5]:
			# for mid, movie in movies.iteritems():
				# if mid == top_recom:
					# print movie(top_recom)
	
	# for user, user_ratings in prefs.iteritems():
		# recommendations = getRecommendations(user, my_user)
		# for bottom_recom in recommendations[:5]:
			# for mid, movie in movies.iteritems():
				# if mid == bottom_recom:
					# print movie(bottom_recom)
					