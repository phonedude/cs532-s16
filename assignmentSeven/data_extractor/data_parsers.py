import threading as Thread 
import threading 
import datetime
import sys 

class Rating_List_Parser(threading.Thread):
	def __init__(self,rating_File_Name):
		threading.Thread.__init__(self)
		self.rating_File_Name = rating_File_Name
		self.ratings = []

	def run(self):
		fileN = None 
		# Attempt to open the file 
		try:
			fileN = open(self.rating_File_Name,'r')
		except IOError as e:
			sys.stdout.write('Error opening file {0}, {1}\n'.format(self.rating_File_Name,e[1]))
			sys.stdout.flush()

		if fileN is not None:
			for line in fileN.readlines():
				strippedLine = line.strip('\n')
				# Split the line into
				tmp = strippedLine.split()
				timeS = float(tmp[3])
				timeConvert = datetime.datetime.utcfromtimestamp(timeS).timetuple()
				timeVal = {'year':timeConvert.tm_year,'month':timeConvert.tm_mon,'day':timeConvert.tm_mday,'hour':timeConvert.tm_hour,'minute':timeConvert.tm_min,'second':timeConvert.tm_sec}


				# Create a data point 
				#dataPoint = {'user_id':tmp[0],'item_id':tmp[1],'rating':float(tmp[2]),'timestamp':float(tmp[3]),'converted_time_stamp':timeVal}
				dataPoint = {'user_id':int(tmp[0]),'item_id':int(tmp[1]),'rating':float(tmp[2]),'timestamp':float(tmp[3]),'converted_time_stamp':timeVal}
				#print(dataPoint)
				# Add the data point to the list of data 
				self.ratings.append(dataPoint)

			fileN.close()

	@property
	def rating_list(self):
		return self.ratings


class Movie_List_Parser(threading.Thread):
	def __init__(self,movie_File_Name):
		threading.Thread.__init__(self)
		self.movie_File_Name = movie_File_Name
		self.movieList = []


	def run(self):
		fileN = None 
		# Attempt to open the file.
		try:
			fileN = open(self.movie_File_Name,'r')
		except IOError as e:
			sys.stdout.write('Error opening file {0}, {1}\n'.format(self.movie_File_Name,e[1]))
			sys.stdout.flush()

		if fileN is not None:
			for line in fileN.readlines():
				strippedLine = line.strip('\n')
				# Split the line into
				tmp = strippedLine.split('|')
				dataPoint = {'movie_id': int(tmp[0]),
					 'movie_title': tmp[1],
					 'release_date': tmp[2],
					 'video_release_date': tmp[3],
					 'IMDb_URL': tmp[4],
					 'unknown': int(tmp[5]),
					 'Action': int(tmp[6]),
					 'Adventure': int(tmp[7]),
					 'Animation': int(tmp[8]),
					 'Childrens': int(tmp[9]),
					 'Comedy': int(tmp[10]),
					 'Crime': int(tmp[11]),
					 'Documentary': int(tmp[12]),
					 'Drama': int(tmp[13]),
					 'Fantasy': int(tmp[14]),
					 'Film-Noir': int(tmp[15]),
					 'Horror': int(tmp[16]),
					 'Musical': int(tmp[17]),
					 'Mystery': int(tmp[18]),
					 'Romance': int(tmp[19]),
					 'Sci-Fi': int(tmp[20]),
					 'War': int(tmp[21]),
					 'Western': int(tmp[22])}
				# Add the data point to the list of data 
				self.movieList.append(dataPoint)

			fileN.close()

	@property 
	def movie_list(self):
		return self.movieList

class Critic_Parser(threading.Thread):
	def __init__(self,critic_File_name):
		threading.Thread.__init__(self)
		self.critic_File_name = critic_File_name
		self.criticList = []

	def run(self):
		fileN = None 

		# Attempt to open the file 
		try:
			fileN = open(self.critic_File_name,'r')
		except IOError as e:
			sys.stdout.write('Error opening file {0}, {1}\n'.format(self.critic_File_name,e[1]))
			sys.stdout.flush()

		if fileN is not None:
			for line in fileN.readlines():
				# Strip the newline character
				strippedLine = line.strip('\n')
				
				# Split the line into
				tmp = strippedLine.split('|')

				dataPoint = {'user_id':int(tmp[0]),'age':int(tmp[1]),'gender':tmp[2],'occupation':tmp[3],'zipcode':tmp[4]}
				
				# Add the data point to the list of data 
				self.criticList.append(dataPoint)

			fileN.close()

	@property 
	def critic_list(self):
		return self.criticList