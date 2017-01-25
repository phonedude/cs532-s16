#! /usr/bin/Rscript

data <- read.table("D:/cs532/a10/q3/results", header=TRUE, comment.char="")
counts <- table(data$Mementos)
pdf("histogram.pdf")
barplot(counts, log="y", ylim=c(.75, nrow(data)), ylab="Memento Count Difference", xlab="Sites", main="Memento Count Difference per Site")
dev.off()