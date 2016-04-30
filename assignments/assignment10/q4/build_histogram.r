#! /usr/bin/Rscript

data <- read.table("D:/cs532/a10/q4/results", header=TRUE, comment.char="")
counts <- table(data$Difference)
pdf("histogram.pdf")
barplot(counts,ylim=c(0.75, nrow(data)), ylab="File Size Difference", xlab="Processed Files", main="Change in Size of Processed File")
dev.off()