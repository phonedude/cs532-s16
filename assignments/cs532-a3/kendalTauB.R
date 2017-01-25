library(Kendall)
setwd(getwd())

d <- read.csv("prtfidf.csv")

# use the library Kendall to see what it says
k<- Kendall(d$PageRank,d$TFIDF)
print(k)

print(summary(k))

corr<-cor(d$PageRank,d$TFIDF ,method="kendall", use="pairwise")
print(corr)

tfidf <- as.numeric(factor(d$TFIDF))
pagerank <- as.numeric(factor(d$PageRank))

m <- cbind(pagerank, tfidf) 

print(cor(m, method="kendall", use="pairwise")) 

print(cor.test(pagerank, tfidf, method="kendall")) 