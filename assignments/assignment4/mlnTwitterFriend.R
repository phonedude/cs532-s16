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


# same as twitter except for one small change ;)
data <- read.csv("mlntwfollowing.csv")
data <- data[order(data$count),]
data$fseq <- seq(1, length(data$count), by = 1)
names(data) <- c("follower","fc","fseq")

#find mln
mln = data[which(data$follower == 'phonedude_mln'),]$fc
numltmln <- with(data,sum(fc < mln))
numgtmln <- with(data,sum(fc > mln))
totalCount <- length(data$fc)

print(paste("@phonedude_mln has less twitter friends than ",as.character(round((numgtmln/totalCount)*100,digits = 2)),"% of his friends"))
print(paste("@phonedude_mln has more twitter friends than ",as.character(round((numltmln/totalCount)*100,digits = 2)),"% of his friends"))

nomln <- subset(data,follower != "phonedude_mln")
twitmean <- round(mean(nomln$fc),digits = 3)
twitmedian <- round(median(nomln$fc),digits = 3)
twitstdev <- round(sd(nomln$fc),digits = 3)
#add log scale so that we can see all the data nicely
data$fc <- log10(data$fc)
xpos = median(data$fseq)
ypos = max(data$fc)
mln = data[which(data$follower == 'phonedude_mln'),]$fseq
ggplot(data,aes(fseq,fc)) +
  geom_bar(
    data = subset(data,follower != "phonedude_mln"),stat = "identity", width =
      0.7, position = position_dodge(0.7)
  ) +
  geom_bar(
    data = subset(data,follower == "phonedude_mln"),fill = "red",stat = "identity", width =
      0.7, position = position_dodge(0.7)
  ) +
  scale_x_continuous(breaks = seq(
    from = 0,to = max(data$fseq),by = 5
  )) + 
  geom_text(
    aes(label =
          ifelse(
            follower == "phonedude_mln",'@phonedude_mln',
            ''
          )),vjust = -6,color = "red",nudge_x = -3.5
  ) +
  geom_vline(xintercept = mln,linetype = 2,color = "red") +
  labs(title = "@phonedude_mln Twitter Friends",x = "Followers of Friends Count",y =
         "Number of Friends")
multiplot(a)
print(paste("mean twitter friend followers=",as.character(twitmean)))
print(paste("median twitter friend followers=",as.character(twitmedian)))
print(paste("stdev twitter friend followers=",as.character(twitstdev)))
