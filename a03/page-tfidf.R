max_x <- max(page.tfidf.data$V1)
max_y <- max(page.tfidf.data$V2)
plot(page.tfidf.data, main="Page Ranking vs TFIDF Ranking Graph", xlab = "Page Ranking", ylab = "TFIDF Ranking")
