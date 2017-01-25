#! /usr/bin/Rscript

# read data
data <- read.table('D:/cs532/a4/q3/linkedin_count', sep=",")
x <- seq(1, length(data$V1))
y <- data$V1

# get notable values
idx <- grep("Naina Sai Tipparti", data$V2)
med_val <- median(data$V1)
med_idx <- which(abs(y - med_val) == min(abs(y - med_val)))
mean_val <- mean(data$V1)
mean_idx <- which(abs(y - mean_val) == min(abs(y - mean_val)))
std_dev <- sd(data$V1)

# draw the graph
pdf("D:/cs532/a4/q3/linkedin_plot.pdf")
plot(x, y, type="l", log="y", pch=10, main="Naina Sai Tipparti Linkedin Friends", 
	ylab="Number of Friends", xlab="Index of Friends")

# illustrate points of interest
abline(h=data$V1[idx], col="red")

# The Legend of the Data
legend(x=82, y=5, cex=0.8, lty=c(1, 1),
	col=c("red", "white", "white", "white", "white"),
	c(paste("Naina Sai Tipparti: ", data$V1[idx]), paste("median: ", med_val), 
		paste("mean: ", format(round(mean_val, 4), nsmall = 4)),
		paste("std dev: ", format(round(std_dev, 4), nsmall = 4)),
		paste("median + 1 std dev: ", format(round(med_val + std_dev, 4), nsmall = 4))))
dev.off()