twitter_paradox -> data
n <- length(data$Followers)
x <- c(1:n)
max_y <- max(data$Followers)
max_x <- length(data$Friend)

plot(data$Followers,  log="y", main="Twitter Friendship Paradox for my Sister\n(Follower Version)", xlab = "Followers", ylab = "Number of Followers (Log Scale)", ylim=range(1,max_y), axes = FALSE, type="l", lwd=2 )
#
# Draw x-axis
#axis(1, at=1:max_x, lab=data$Friend, pos = 1)
axis(1, at=c(seq(1,max_x, 3), 33), lab=data$Friend[c(seq(1, length(data$Friend), 3), 33)])
#
# Draw y-axis
y_data <- c(2,4,8,100,1000,10000,200000)
options("scipen"=100, "digits"=4)
axis(2, las=1, at=y_data, pos = 0.5)

y.med <- median(data$Followers)
y.mean <- mean(data$Followers)
data_sd <- sd(data$Followers)
x.med <- 17
x.mean <- 30 - (6504 - y.mean) / (6504 - 1066) + .12
temp <- mapply(function(x,y,c) lines(c(x,x), c(2,y), lwd=2, col=c), c(x.mean, x.med), c(y.mean, y.med), c("Blue", "Gray"))
text(x.mean - 1, y.mean+1000, paste("mean ", round(y.mean, 2)), cex=0.7)
text(x.med, y.med+30, paste("median ", y.med), cex=0.7)
     