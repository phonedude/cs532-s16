
from data_parsers import Rating_List_Parser, Movie_List_Parser, Critic_Parser


# ADT to manage the dataset 
class Data_Set:
	def __init__(self,ratingListFileName='./data/movielens/u.data',movieListFileName='./data/movielens/u.item',criticListFileName='./data/movielens/u.user'):
		self.rating_list = []
		self.movie_list = []
		self.critic_list = []

		parserList = [Rating_List_Parser(ratingListFileName),Movie_List_Parser(movieListFileName),Critic_Parser(criticListFileName)]

		for thread in parserList:
			thread.run()

		# Wait for the threads to finish
		while True:
			if len(list(filter(lambda t: t.is_alive(),parserList))) == 0:
				break 

		# Retrieve the results from the threads 
		self.rating_list = parserList[0].ratings 
		self.movie_list = parserList[1].movie_list
		self.critic_list = parserList[2].critic_list


	@property 
	def rating_list(self):
		return self.rating_list

	@property 
	def movie_list(self):
		return self.movie_list

	@property 
	def critic_list(self):
		return self.critic_list




if __name__ == '__main__':
	data = Data_Set()
	print(len(data.movie_list))

