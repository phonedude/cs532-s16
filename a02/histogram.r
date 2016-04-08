histogramdata[with(histogramdata, order(count)), ] -> data
max_x <- max(data$count)
max_y <- max(data$No.URI)
barplot(data$No.URI, log="y", main="Memento Histogram", col=heat.colors(6), xlab = "Mementos Count", ylab = "Number of URIs", names.arg = data$count )
text(2,800, "860", cex=0.7)
text(20,30, "31", cex=0.7)
text(27,10, "11", cex=0.7)
text(28,2.7, "3", cex=0.7)
