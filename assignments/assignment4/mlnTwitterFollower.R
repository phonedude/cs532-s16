library(ggplot2)
options(scipen = 9999)
setwd(getwd())


#this function wonderfully borowed from
#http://www.cookbook-r.com/Graphs/Multiple_graphs_on_one_page_%28ggplot2%29/
multiplot <-
  function(..., plotlist = NULL, file, cols = 1, layout = NULL) {
    library(grid)
    # Make a list from the ... arguments and plotlist
    plots <- c(list(...), plotlist)
    numPlots = length(plots)
    # If layout is NULL, then use 'cols' to determine layout
    if (is.null(layout)) {
      # Make the panel
      # ncol: Number of columns of plots
      # nrow: Number of rows needed, calculated from # of cols
      layout <- matrix(seq(1, cols * ceiling(numPlots / cols)),
                       ncol = cols, nrow = ceiling(numPlots / cols))
    }
    if (numPlots == 1) {
      print(plots[[1]])
      
    } else {
      # Set up the page
      grid.newpage()
      pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
      
      # Make each plot, in the correct location
      for (i in 1:numPlots) {
        # Get the i,j matrix positions of the regions that contain this subplot
        matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
        
        print(plots[[i]], vp = viewport(
          layout.pos.row = matchidx$row,
          layout.pos.col = matchidx$col
        ))
      }
    }
  }


# read the data
data <- read.csv("mlntwfollers.csv")

# i got smarter here

# order the data
data <- data[order(data$count),]

# add friend sequence numbers for x-axis
data$fseq <- seq(1, length(data$count), by = 1)

# change column names
names(data) <- c("follower","fc","fseq")

#find mln
mln = data[which(data$follower== 'phonedude_mln'),]$fc
numltmln <- with(data,sum(fc < mln))
numgtmln <- with(data,sum(fc > mln))
totalCount <- length(data$fc)
print(paste("phonedude_mln has less twitter followers than ",as.character(round((numgtmln/totalCount)*100,digits = 2)),"% of his followers"))
print(paste("phonedude_mln has more twitter followers than ",as.character(round((numltmln/totalCount)*100,digits = 2)),"% of his followers"))

# remove mln
nomln <- subset(data,follower != "phonedude_mln")
# get stats
twitmean <- round(mean(nomln$fc),digits = 3)
twitmedian <- round(median(nomln$fc),digits = 3)
twitstdev <- round(sd(nomln$fc),digits = 3)


data$fc <- log10(data$fc)



# get plot a mln is here and we are plotting less than or equal to mid
# get positon for stats annotation
xpos = median(data$fseq)
ypos = max(data$fc)
# where are you on the x-axis mln ?
mln = data[which(data$follower == 'phonedude_mln'),]$fseq
a<-ggplot(data,aes(fseq,fc)) +  
  geom_bar(data = subset(data,follower != "phonedude_mln"),stat = "identity", width =
             0.7, position = position_dodge(0.7)
  ) +
  geom_bar(
    data = subset(data,follower == "phonedude_mln"),fill = "red",stat = "identity", width =
      0.7, position = position_dodge(0.7)
  ) +
  scale_x_continuous(breaks = seq(
    from = 0,to = max(data$fseq),by = 20
  )) + 
  # add mln text marker since it is larger than simply mln add some sanity
  geom_text(
    aes(label =
          ifelse(
            follower == "phonedude_mln",'@phonedude_mln',
            ''
          )),vjust = -6,color = "red",nudge_x = -35
  ) +
  # explicitly add line to where mln is
  geom_vline(xintercept = mln,linetype = 2,color = "red") +
  labs(title = "@phonedude_mln Twitter Follower count",x = "Friends of Followers Count",y = "Number of Friends")

pdf("mlnTwitterParadox.pdf")
multiplot(a)
dev.off()


print(paste("mean followers=",as.character(twitmean)))
print(paste("median followers=",as.character(twitmedian)))
print(paste("stdev followers=",as.character(twitstdev)))
