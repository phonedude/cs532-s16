#! /usr/bin/Rscript

# read data
data <- read.table('D:/cs532/a4/q2/followers_counts')
x <- seq(1, length(data$V1))
y <- data$V1

# get notable values
mln_idx <- grep("phonedude_mln", data$V2)
med_val <- median(data$V1)
med_idx <- which(abs(y - med_val) == min(abs(y - med_val)))
mean_val <- mean(data$V1)
mean_idx <- which(abs(y - mean_val) == min(abs(y - mean_val)))
std_dev <- sd(data$V1)

# draw the graph
pdf("D:/cs532/a4/q2/followers_plot.pdf")
plot(x, y, type="l", log="y", pch=19, main="Dr. Nelson's Friends' Friends", 
	ylab="Number of Friends", xlab="Index of Friend")

# illustrate points of interest
abline(h=data$V1[mln_idx], col="red")

# The Legend of the Data
legend(x=82, y=5, cex=0.8, lty=c(1, 1),
	col=c("red", "white", "white", "white", "white"),
	c(paste("Nelson: ", data$V1[mln_idx]), paste("median: ", med_val), 
		paste("mean: ", format(round(mean_val, 4), nsmall = 4)),
		paste("std dev: ", format(round(std_dev, 4), nsmall = 4)),
		paste("median + 1 std dev: ", format(round(med_val + std_dev, 4), nsmall = 4))))
dev.off()