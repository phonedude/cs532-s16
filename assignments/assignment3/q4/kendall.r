#! /usr/bin/Rscript

library(Kendall)
data <- read.table("D:/cs532/a3/q4/kendall", header=TRUE)
tfidf <- data[1]
pagerank <- data[2]
cor(tfidf, pagerank, method="kendall")
Kendall(tfidf,pagerank)
