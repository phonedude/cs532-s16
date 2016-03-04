library(igraph)
library(igraphdata)

#ok so lets do this in R
data(karate)
karateClub <- karate
#hmmm this looks interesting
#edge.betweenness.community(cluster_edge_betweenness),65 from the pdf on cran
ceb <- cluster_edge_betweenness(karateClub)
#what does this give us a communities class
print(class(ceb))
#look what we have here! it removed edges for us well sorta
print(ceb$removed.edges)
#this will print edge betweenness ;)
print(ceb$algorithm)

#set to true to see debug output
debug <- TRUE

#how many communities do we wish to split to
splitTo <- 2

#ok some set up
#want to preserve the final graph that we create
# I will not be touching the original karate club
finalPlot <- karateClub
plot.igraph(finalPlot)

#ok so I want have a counter to keep track 
#of where I am in the algorithm
removeIndex <- 1
#use the same scheme as python I want to make sure
#the number of connected componets are less than 2
#for the Zachary Analysis 
numConnected <- count_components(karateClub)

#loop
while(numConnected < splitTo){
  #ok so this feels like cheating here
  #the scheme is to progressively remove edges the ebc communities class calculated for us
  #if you start at index 0 you get nothing so I start at 1 to removeIndex -1 
  #base removeIndex=1 seq(1,removeIndex-1) yeild 1 0 
  #so the ebc$removed.edges[seq(1,removeIndex-1) ] yeild edge at pos 1 :)
  deletedG <- delete.edges(karateClub, ceb$removed.edges[seq(1,removeIndex-1)])
  #deleteG is now the result of iteration N of Girvan–Newman 
  
  #increment our iteration of Girvan–Newman up by one
  removeIndex <- removeIndex + 1
  # plot.igraph(deletedG)
  if(debug){
    print(seq(1,removeIndex-1))
    print(ceb$edge.betweenness[seq(1,removeIndex-1)])
    print(ceb$removed.edges[seq(1,removeIndex-1)])
    print("+++++++++++++++++++++++++++++")
  }
  #get the number of connected componets ie 
  #have we split the graph into two subgraphs
  numConnected <- count_components(deletedG)
  finalPlot <- deletedG
}

plot.igraph(finalPlot)
