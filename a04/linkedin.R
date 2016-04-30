linkedin.paradox[order(linkedin.paradox$Connection),] -> ddata
n <- length(ddata)
x <- c(1:n)
max_y <- max(ddata)

plot(ddata,  main="Linkedin Friendship Paradox for my Wife", xlab = "Connection", ylab = "Number of Connections", ylim=range(1,max_y), axes = FALSE, type="l", lwd=2 )
#
# Draw x-axis
#axis(1, at=c(seq(1,max_x, 3), 33), lab=ddata$Friend[c(seq(1, length(ddata$Friend), 3), 33)])
x_label <- paste("c", c(seq(1,n, 4)))
x_label[2] <- "Wife"
axis(1, at=c(seq(1,n, 4)), lab=x_label)
#
# Draw y-axis
y_data <- c(6,50,100,150,200,250,300,350,400, 450,500)
options("scipen"=100, "digits"=4)
axis(2, las=1, at=y_data, pos = 0.5)

y.med <- median(ddata)
y.mean <- mean(ddata)
data_sd <- sd(ddata)
x.med <- 35
x.mean <- 33 - (346 - y.mean) / (346 - 335) + .12
temp <- mapply(function(x,y,c) lines(c(x,x), c(2,y), lwd=2, col=c), c(x.mean, x.med), c(y.mean, y.med), c("Blue", "Gray"))
text(x.mean - 1, y.mean+20, paste("mean ", round(y.mean, 2)), cex=0.7)
text(x.med - 1, y.med+10, paste("median ", y.med), cex=0.7)
     