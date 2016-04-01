import recommendations

open('correlationOutput.txt', 'w')

#to make sure that the file is clean
reload(recommendations)

MyAlternate = '603'

MovieLensDataset = recommendations.loadMovieLens()

with open('./data/numberFile.txt') as f: 
    lines = f.readlines()
    lines = [x.strip('\n') for x in lines]

for users in lines:
    #outputFile.write("for Id: " + str(twIds))
    #outputFile.write("\n")
	print recommendations.sim_pearson(MovieLensDataset, '603', int(users))


#print recommendations.sim_pearson(MovieLensDataset, '603', '604')