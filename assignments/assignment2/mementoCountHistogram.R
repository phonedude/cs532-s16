# set the working directory
setwd(getwd())
# get dataframe site,count
mementoCount <- read.csv('counted.csv')
# make histogram
h <- hist(mementoCount$count,main="Histogram of Memento Counts",xlab = "Count")
# add count labels
text(h$mids,h$counts,labels=h$counts, adj=c(0.5, -0.5))
