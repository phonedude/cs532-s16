import argparse 
import logging 
import sys 
#NOTE: THIS PROGRAM WAS CREATED BY KEVIN CLEMMONS. ALL CREDIT IS GIVEN TO HIM
from data_extractor.data_set import Data_Set

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',datefmt='%m-%d %H:%M:%S',filename='subsitute_you.log',filemode='w+')

defaultLogger = logging.getLogger('default')



def get_prefs(data):
	'''Create a dictionary of people and the movies that they have rated. 
	'''
	# This code taken from page 26 in collective intelligence book

	movies = {}
	for movie in data.movie_list:
		movie_id = movie['movie_id'] 
		movie_title = movie['movie_title']
		movies[movie_id] = movie_title

	prefs = {}

	for dataPoint in data.rating_list:
		user_id = int(dataPoint['user_id'])
		movieId = dataPoint['item_id']
		rating = dataPoint['rating']
		prefs.setdefault(user_id,{})
		prefs[user_id][movies[movieId]] = float(rating)
	return prefs

# Returns the best matches for person from the prefs dictionary. 
# Number of results and similarity function are optional params.
#def topMatches(prefs,person,n=5,similarity=sim_pearson):
#  scores=[(similarity(prefs,person,other),other) 
                  #for other in prefs if other!=person]
#  scores.sort()
#  scores.reverse()
#  return scores[0:n]

def printResults(similarUsers):
	seperator = '-----------------------------------------------------'
	heading1 =  '-----------------------Top-3-------------------------'
	heading2 =  '--------------------Bottom-Three---------------------'
	heading3 =  '----------------------Summary------------------------'
	heading0 =  '--------------------Similar Users--------------------'
	print(heading0)
	for key in similarUsers.keys():
		
		print("User: {0}:".format(key))
		#print(seperator)
		print(heading1)
		#print("Top 3:")

		counter = 1
		for topThree in similarUsers[key]['top_three_favorite']:
			print("{0}){1:.<48}{2}".format(counter,topThree['movie_title'],topThree['rating']))
			counter += 1
		counter = 1

		print(heading2)
		for bottomThree in similarUsers[key]['bottom_three_favorite']:
			print("{0}){1:.<48}{2}".format(counter,bottomThree['movie_title'],bottomThree['rating']))
			counter += 1
		
		print(seperator)
		print(seperator)
	print(heading3)
	print("{0:.<52}{1}".format('Number of Users',len(similarUsers)))

def get_user_match(data,name=None,gender=None,age=None,occupation=None):
	# Default values if gender, age or occupation are not passed in.
	_name = 'User'
	_gender = 'M'
	_age = 21
	_occupation = 'student'

	if name:
		_name = name

	if gender:
		_gender = gender
	
	if age:
		_age = age

	if occupation:
		_occupation = occupation



	
	# Create a dictionary of users and the movies that they rated.
	prefs = get_prefs(data) 
	

	similarUsers = list(filter(lambda x: x['age'] == _age and x['gender'] == _gender and x['occupation'] == _occupation,data.critic_list))
	defaultLogger.info("{0} similar users found".format(len(similarUsers)))
	
	# Ensure that there are at least 3 similar users found in the filter. 

	userInformation = {}

	for i in similarUsers:
		user_id = int(i['user_id'])

		defaultLogger.debug("Getting movie ratings for user: {0}".format(user_id))
		userPrefs = prefs[user_id]
		defaultLogger.debug("{0} movie ratings found for user: {0}".format(len(userPrefs),user_id))

		# Create a list that can be sorted on rating id 
		defaultLogger.debug("Creating list that can be sorted for user: {0}".format(user_id))
		movieRankingList = []
		for movie in userPrefs.keys():
			movieTitle = movie
			rating = userPrefs[movie]
			movieRankingList.append({'movie_title':movieTitle,'rating':rating})

		lowestToHigh = sorted(movieRankingList,key=lambda x: x['rating'],reverse=False)
		highestToLow = sorted(movieRankingList,key=lambda x: x['rating'],reverse=True)
		defaultLogger.info("Determining top three favorite movies and top three least favorite films for user: {0}".format(user_id))
		userInformation[user_id] = {'top_three_favorite':highestToLow[:3], 'bottom_three_favorite':lowestToHigh[:3]}
	return userInformation


if __name__ == '__main__':
	gender = None
	age = None 
	occupation = None
	name=None
	occupationFileName = './data/movielens/u.occupation'
	data = Data_Set()
	

	try:
		occupationFile = open(occupationFileName,'r')
	except IOError as e:
		defaultLogger.error("Error getting occupation list file: {0},{1}".format(occupationFileName,e[1]))
		print("Error getting occupation list file: {0},{1}".format(occupationFileName,e[1]))
	
	if occupationFile is not None:
		# Create a list of valid occupations 
		occupationList = [line.strip('\n') for line in occupationFile.readlines() ]
		occupationFile.close() 

		# Parse the command-line arguments 
		parser = argparse.ArgumentParser(description='Finds three users who are closest to you in terms of age, gender, and occupation')
		parser.add_argument('-n','--name',action='store',dest='name',help='Your Name')
		parser.add_argument('-a','--age',action='store',dest='age',help='Your age.')
		parser.add_argument('-g','--gender',choices=['m','f','male','female'],dest='gender',help='Gender of the user')
		parser.add_argument('-o','--occupation',choices=occupationList, dest='occupation', help='Occupation')

		args = parser.parse_args()

		if args.name:
			name = args.name
			defaultLogger.info("Using custom name: {0}".format(name))
		else:
			defaultLogger.info("Using default name: User")
		
		if args.age:
			age = int(args.age)
			defaultLogger.info("Using custom age: {0}".format(age))
		else:
			defaultLogger.info("Using default age: 21")

		if args.gender:
			defaultLogger.info("Using custom gender: {0}".format(args.gender))
			if args.gender == 'm' or args.gender =='male':
				gender = 'M'
				defaultLogger.debug("gender set to: M")
				

			if args.gender == 'f' or args.gender == 'female':
				gender = 'F'
				defaultLogger.debug("gender set to: F")
		else:
			defaultLogger.info("Using default gender: M")

		if args.occupation:
			defaultLogger.info("Custom occupation given: {0}".format(occupation))
			occupation = args.occupation
		else:
			defaultLogger.info("Using default occupation: student")

		# Get a match of the users
		result = get_user_match(data,name=name,gender=gender,age=age,occupation=occupation)
		printResults(result)
	#print("Hello")

