#! /usr/bin/Rscript

data <- read.table("D:/cs532/q3/ecd_mementos", header=TRUE)
strtodate = function(x) {
	result = Sys.time() - strptime(x, "%Y-%m-%dT%H:%M:%S")
	return(result)
}
data$ECD <- lapply(data$ECD, strtodate)
pdf("ecd_mementos.pdf")
plot(data, log="y", xlab="Estimated Site Age in days", ylab="Number of Mementos", main="Estimated Site Age to Memento Count")
dev.off()