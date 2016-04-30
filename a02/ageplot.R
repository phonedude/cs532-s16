age.memeto.data[with(age.memeto.data, order(Age)), ] -> age_memento
max_x <- max(age_memento$Age)
max_y <- max(age_memento$MementoQty)
plot(age_memento,log="xy", main="Age vs Memento Graph", xlab = "Estimated URI Age in Days", ylab = "Number of URI Mementos")
# plot(age_memento,log="xy", main="Age vs Memento Graph", xlab = "Estimated URI Age in Days", ylab = "Number of URI Mementos", cex = 1.5, pch=18, col='orange')
# data.frame(unique(data.frame(age_memento$Age, age_memento$MementoQty))) no-repeated data set
as.data.frame(table(age_memento)) -> d
data.frame(d[with(d, order(Age)),]) -> t
t[t$Freq != 0,] -> d
plot(t, log="xy", main="Age vs Memento Graph", xlab = "Estimated URI Age in Days", ylab = "Number of URI Mementos", cex = c(d$Freq), pch=18, col='orange')
