ffriendship_paradox -> data
n <- length(data$No.Friends)
max_y <- max(data$No.Friends)
max_x <- length(data$Friend)
y_data <- c(1, 500, 1000, 1500, 2000, 2500, 3000, 3200)
plot(data$No.Friends,  main="Friendship Paradox for Dr. Nelson", xlab = "Friends", ylab = "Number of Friends", ylim=range(1,max_y), axes = FALSE, type="l", lwd=2 )
axis(1, at=c(1, seq(4,max_x,10)), lab=data$Friend[c(1, seq(4, length(data$Friend), 10))])
axis(2, las=1, at=y_data, pos = 0.5)
x <- c(1:max_x)
y.mean <- mean(data$No.Friends)
y.med <- median(data$No.Friends)
data_sd <- sd(data$No.Friends)
x.med <- 78
x.mean <- 100 + (359-y.mean) / 6
temp <- mapply(function(x,y,c) lines(c(x,x), c(0,y), lwd=2, col=c), c(x.mean, x.med), c(y.mean, y.med), c("Blue", "Gray"))
text(x.mean, y.mean+70, paste("mean ", round(mean(data$No.Friends)), 2), cex=0.7)
text(x.med, y.med+60, paste("median ", median(data$No.Friends)), cex=0.7)
