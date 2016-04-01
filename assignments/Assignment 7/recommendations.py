from math import sqrt

def loadMovieLens(path='/data'):
	#Get movie titles
	movies={}
	for line in open('u.item'):
		(id,title)=line.split('|')[0:2]
		movies[id]=title
	#Load data
	prefs={}
	for line in open('u.data'):
		(user,movieid,rating,ts)=line.split('\t')
		prefs.setdefault(user,{})
		prefs[user][movies[movieid]]=float(rating)
	return prefs

def sim_pearson(prefs,p1,p2):
	#Get the list of mutually rated items
	si={}
	for item in prefs[p1]:
		if (item in prefs[p2]):
			si[item]=1
	#Find the number of elements
	n=len(si)
	#If there are no ratings in common, return 0
	if n==0: return 0
	#Add up all the preferences
	sum1=sum([prefs[p1][it] for it in si])
	sum2=sum([prefs[p2][it] for it in si])
	#Sum up the squares
	sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
	sum2Sq=sum([pow(prefs[p2][it],2) for it in si])
	#Sum up the products
	pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
	#Calculate Pearson score
	num=pSum-(sum1*sum2/n)
	den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
	if (den==0):
		return 0
	r=num/den
	return r

def topMatches(prefs,person,n=5,similarity=sim_pearson):
	scores=[(similarity(prefs,person,other),other) 
					for other in prefs if other!=person]
	#Sort the list so the highest scores appear at the top
	scores.sort()
#	scores.sort(reverse=True)
	scores.reverse()
	return scores[0:n]


#Gets recommendations for a person by using a weighted average
#of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
	totals={}
	simSums={}
	for other in prefs:
		#don't compare me to myself
		if other==person: continue
		sim=similarity(prefs,person,other)
		#ignore scores of zero or lower
		if sim<=0: continue
		for item in prefs[other]:
			#only score movies I haven't seen yet
			if item not in prefs[person] or prefs[person][item]==0:
				#Similarty * Score
				totals.setdefault(item,0)
				totals[item]+=prefs[other][item]*sim
				#Sum of similarities
				simSums.setdefault(item,0)
				simSums[item]+=sim
	#Create the normalized list
	rankings=[(total/simSums[item],item) for item,total in totals.items()]
	#Return the sorted list
	rankings.sort()
	rankings.reverse()
	return rankings

def transformPrefs(prefs):
	result={}
	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item, {})
			#Flip item and person
			result[item][person]=prefs[person][item]
	return result

if __name__ == '__main__':
	prefs=loadMovieLens()
#	print (prefs['372'])
#	print sim_pearson(prefs, '372', '1')
#	for i in range (1,944):
#		print str(i), sim_pearson(prefs, '372', str(i))
#	print topMatches(prefs,'372')
#	print getRecommendations(prefs,'372')
	movies=transformPrefs(prefs)
	print topMatches(movies, 'Crow, The (1994)')
#	print topMatches(movies, 'Pocahontas (1995)')