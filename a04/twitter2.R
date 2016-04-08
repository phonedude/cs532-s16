twitter_paradox_2 -> data

n <- length(data$following)
x <- c(1:n)
max_y <- max(data$following)
max_x <- length(data$Friend)

plot(data$following,  log="y", main="Twitter Friendship Paradox for my Sister\n(Following Version)", xlab = "following", ylab = "Following Number (Log Scale)", ylim=range(1,max_y), axes = FALSE, type="l", lwd=2 )
#
# Draw x-axis
#axis(1, at=1:max_x, lab=data$Friend, pos = 1)
axis(1, at=c(seq(1,max_x, 4)), lab=data$Friend[c(seq(1, length(data$Friend), 4))])
#
# Draw y-axis
y_data <- c(1, 2,10, 45,1000,10000, 100700)
options("scipen"=100, "digits"=4)
axis(2, las=1, at=y_data, pos = 0.5)

y.med <- median(data$following)
y.mean <- mean(data$following)
data_sd <- sd(data$following)
sis.x <-9
sis.y <- 71
x.med <- 17
x.mean <- 31 - (6514 - y.mean) / (6544 - 2061) + .12
temp <- mapply(function(x,y,c) lines(c(x,x), c(2,y), lwd=2, col=c), c(x.mean, x.med), c(y.mean, y.med), c("Blue", "Gray"))
text(x.mean - 1, y.mean+1000, paste("mean ", round(y.mean, 2)), cex=0.7)
text(x.med, y.med+30, paste("median ", y.med), cex=0.7)
text(sis.x, sis.y+30, paste("sister ", sis.y), cex=0.7)
     