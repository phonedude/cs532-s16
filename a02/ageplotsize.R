age.memeto.data[with(age.memeto.data, order(Age)), ] -> age_memento
as.data.frame(table(age_memento)) -> d
data.frame(d[with(d, order(Age)),]) -> t
t[t$Freq != 0,] -> d
plot(data$Age, data$MementoQty,log="xy", main="Age vs Memento Graph", xlab = "Estimated URI Age in Days", ylab = "Number of URI Mementos", cex = log(data$Freq)/2+1, col=data$Freq+1, pch=16)
