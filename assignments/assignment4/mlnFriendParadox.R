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


  # read the datfile
  data <- read.csv("mlnfbcount.csv")
  #get the friend count
  frinedCount <- sort(data$fcount)
  #find mln
  mln = data[which(data$friend == 'mln'),]$fcount
  numltmln <- with(data,sum(fcount < mln))
  numgtmln <- with(data,sum(fcount > mln))
  totalCount <- length(data$fcount)
  
  print(paste("mln has less fb friends than ",as.character(round((numgtmln/totalCount)*100,digits = 2)),"% of his friends"))
  print(paste("mln has more fb friends than ",as.character(round((numltmln/totalCount)*100,digits = 2)),"% of his friends"))
  
  #create plot dataframe
  dplot <-
    data.frame(seq(1, length(frinedCount), by = 1),frinedCount)
  #change column names
  names(dplot) <- c("fseq","fc")
  #remove mln for stats
  nomln <- subset(data,friend != "mln")
  
  #find number of friends
  numFriends <- length(data$friends)
  
  #do stats
  fbcmean <- round(mean(nomln$fcount),digits = 3)
  fbcmedian <- round(median(nomln$fcount),digits = 3)
  fbcstdev <- round(sd(nomln$fcount),digits = 3)
  
  #inform user
  print(paste("mln mean fb friends=",as.character(fbcmean)))
  print(paste("mln media fb friends=",as.character(fbcmedian)))
  print(paste("mln stdev fb friends=",as.character(fbcstdev)))
  print("---------------------------------")
  # find position for the text annotations
  xpos <- median(dplot$fseq)
  ypos <- median(dplot$fc)
 
  
  # do the plot
  a <- ggplot(dplot,aes(fseq,fc)) +
    # scale x to see the number of friends mln has
    scale_x_continuous(breaks = seq(
      from = 0,to = max(dplot$fc),by = 15
    )) +
    # plot data first plot regular  data the plot and highlight mln
    geom_bar(
      data = subset(dplot,fc != mln),stat = "identity", width = 0.5, position =
        position_dodge(0.7)
    ) +
    geom_bar(
      data = subset(dplot,fc == mln),fill = "red",stat = "identity", width = 0.9, position =
        position_dodge(0.7)
    ) +
    # add annoations
    geom_text(aes(label = ifelse(fc == mln,paste('mln friend count: ',as.character(mln)),'')),vjust = -1) +
    labs(title = "mln Facebook friend count",x = "Friends of Friends Count",y =
           "Number of Friends")
  # save plot to pdf
  pdf("mlnFacebookParadox.pdf")
  multiplot(a)
  dev.off()
  



