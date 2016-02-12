library(ggplot2)
setwd(getwd())

#this function wonderfully borrowed from 
#http://www.cookbook-r.com/Graphs/Multiple_graphs_on_one_page_%28ggplot2%29/
multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  library(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  numPlots = length(plots)
  
  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }
  
  if (numPlots==1) {
    print(plots[[1]])
    
  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
    
    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
      
      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}

# get the age,mementos dataframe
dateNum <- read.csv('dated.csv')

# find the median value to split the plots
mcount <- sort(unique(dateNum$mementos))
midval <- median(mcount)

# find all values less than the midval 
lt <- subset(dateNum, dateNum$mementos <= midval)
# find all values greater than the midval
gt <- subset(dateNum, dateNum$mementos >= midval)

# plot the entire dataframe
# use stat_identity to plot the actual data not a count
a<-ggplot(dateNum,  aes(y=mementos,x=age,color=mementos))+
  geom_bar(stat="identity")+scale_color_identity()+
  ggtitle("All Age Count plotted")

# plot the lower values, use color values based on memento count
b<-ggplot(lt,  aes(y=mementos,x=age,color=mementos))+
  geom_bar(stat="identity",position = "stack",aes(color=mementos))+ 
  ggtitle(as.character("Age Count plotts less than the median"))

# plot the upper values, use color values based on memento count
c<-ggplot(gt,  aes(y=mementos,x=age))+
  geom_bar(stat="identity",position = "stack",aes(color=mementos))+
  scale_fill_identity(breaks = lt$mementos,guide = "legend")+
  ggtitle(as.character("Age Count plotts greater than the median"))

#combine the three plots
multiplot(a,b,c,cols=2)
