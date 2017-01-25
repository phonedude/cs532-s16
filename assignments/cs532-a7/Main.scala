import java.io._
import java.nio.charset.CodingErrorAction
import java.util.StringJoiner

import scala.io.{Codec, Source}
import jberlin._

import scala.collection.mutable


object Main {

  def writeToFile(name: String, lines: mutable.MutableList[String]) = {
    val fout = new File(name)
    val fos = new FileOutputStream(fout)
    val bw = new BufferedWriter(new OutputStreamWriter(fos))
    lines.foreach(l => {
      bw.write(l)
      bw.newLine()
    })

    bw.close()
  }

  def umap(line: String): user = line.split("\\|")

  def urmap(line: String): urating = line.split("\\s+")

  def mvmap(line: String): (Int, movie) = {
    def help(m: movie) = (m.mid, m)
    val ar = line.replaceAll("\\|\\|", "\\|").split("\\|")
    help((ar(0), ar(1)))
  }


  def findCloseToMe(users: List[user]) = {
    val me = 622
    val likeme = users.filter(u => u.age == 25 && u.job.equals("programmer")).slice(1, 4)
    var ml = mutable.MutableList[String]()
    likeme.foreach(u => {
      println(u)
      ml += u.toString
      val mrs = u.mRatings.values.toList.map(ur => (ur.mname, ur.rating)).sortBy(_._2).reverse
      ml += "top three movies: " + mrs.take(3).foldLeft(new StringJoiner(","))((jnr, ur) => jnr.add(ur.toString())).toString
      ml += "bottom three movies: " + mrs.tail.drop(mrs.length - 4).foldLeft(new StringJoiner(","))((jnr, ur) => jnr.add(ur.toString())).toString + "\n"
      println(mrs.take(3))
      println(mrs.tail.drop(mrs.length - 4))
      println("============================")
    })
    writeToFile("top3.txt", ml)
    likeme.slice(2, 3).head
  }

  def persons(likeme: user, u: user): Double = {
    val mkeys = likeme.mRatings.keySet intersect u.mRatings.keySet
    if (mkeys.isEmpty) {
      u.corToMe = 0.0
      return 0.0
    }
    val myMovies = likeme.mRatings.filterKeys(k => mkeys contains k).values.toList.sortBy(_.itemId)
    val otherGuys = u.mRatings.filterKeys(k => mkeys contains k).values.toList.sortBy(_.itemId)

    val (sum1, sum2, sum1sq, sum2sq, sump) = (myMovies zip otherGuys).foldLeft((0.0, 0.0, 0.0, 0.0, 0.0)) {
      case ((as1, as2, asq1, asq2, asp), (mr, ur)) =>
        (as1 + mr.rating, as2 + ur.rating, asq1 + math.pow(mr.rating, 2.0),
          asq2 + math.pow(ur.rating, 2.0), asp + (mr.rating * ur.rating))
    }
    val n = mkeys.size
    val num = sump - (sum1 * sum2 / n)
    val den = math.sqrt((sum1sq - math.pow(sum1, 2.0) / n) * (sum2sq - math.pow(sum2, 2.0) / n))
    val r = if (den == 0) 0.0 else num / den
    u.corToMe = r
    r
  }

  def pMovies(movie:List[(String,Int,Int)],other:List[(String,Int,Int)]) ={
    val (sum1, sum2, sum1sq, sum2sq, sump) = (movie zip other).foldLeft((0.0, 0.0, 0.0, 0.0, 0.0)) {
      case ((as1, as2, asq1, asq2, asp), (mr, ur)) =>
        (as1 + mr._3, as2 + ur._3, asq1 + math.pow(mr._3, 2.0),
          asq2 + math.pow(ur._3, 2.0), asp + (mr._3 * ur._3))
    }
    val n = movie.size
    val num = sump - (sum1 * sum2 / n)
    val den = math.sqrt((sum1sq - math.pow(sum1, 2.0) / n) * (sum2sq - math.pow(sum2, 2.0) / n))
    val r = if (den == 0) 0.0 else num / den
    r
  }



  def correlatedUsers(likeme: user, users: List[user]) = {
    val usrCors = users.filter(u => u.id != likeme.id).map(u => (u, persons(likeme, u))).sortBy(_._2).reverse

    var ml = mutable.MutableList[String]()

    val top5cor = usrCors.take(5)
      .foldLeft(new StringJoiner("\n"))((jnr, uc) => jnr.add(uc._1 + " correlation: " + uc._2)).toString

    ml += "Top 5 correlated users:\n" + top5cor + "\n"

    val bottom5cor = usrCors.tail.drop(usrCors.length - 6)
      .sortBy(_._2).foldLeft(new StringJoiner("\n"))((jnr, uc) => jnr.add(uc._1 + " correlation: " + uc._2))

    ml += "\nBottom 5 correlated users:\n" + bottom5cor + "\n"

    writeToFile("topBottom5Correlated2.txt", ml)

    usrCors
  }

  def movieRecomendations(likeme: user, correlation: List[(user, Double)]) = {
    val mkeys = likeme.mRatings.keySet
    correlation.filter(_._2 > 0.0).flatMap {
      case (usr, cor) =>
        val haventSeen = usr.mRatings.keySet.diff(mkeys)
        usr.mRatings.filterKeys(k => haventSeen contains k)
          .values.toList.sortBy(_.itemId).map { case ur => (ur.itemId, cor, ur.rating * cor) }
    }.groupBy(_._1).map { case (mid, ratings) =>
      val (sumsim, sumweight) = ratings.foldLeft((0.0, 0.0)) {
        case (acum, (movid, cor, ws)) => (acum._1 + cor, acum._2 + ws)
      }
      (mid, sumweight / sumsim)
    }.toList.sortBy(_._2).reverse
  }

  def main(args: Array[String]) {


    val usrfile = "ml-100k/u.user"
    val usrReviews = "ml-100k/u.data"
    val movief = "ml-100k/u.item"

    implicit val codec = Codec("UTF-8")
    codec.onMalformedInput(CodingErrorAction.REPLACE)
    codec.onUnmappableCharacter(CodingErrorAction.REPLACE)

    val users = Source fromFile usrfile getLines() map { case line => umap(line) } toList
    val movies = Source.fromFile(movief).getLines().map { case line => mvmap(line) }.toMap
    val userReviews = Source.fromFile(usrReviews).getLines().map {
      case line =>
        val rating = urmap(line)
        movies.get(rating.itemId) match {
          case Some(m) => rating.mname = m.mtitle
          case None => println("Bad juju movieTitle -> rating")
        }
        rating
    }.toList.groupBy(_.uid)

    users.foreach(u => {
      userReviews.get(u.id) match {
        case Some(ratings: List[urating]) =>
          //          u.mRatings = ratings.sortBy(_.rating).reverse
          u.mRatings = ratings.map(ur => (ur.itemId, ur)).toMap
        case None => println("Bad juju")
      }
    })

    val likeme = findCloseToMe(users)
    val correlation = correlatedUsers(likeme, users)
    val myRecomendation = movieRecomendations(likeme, correlation)
    var ml = mutable.MutableList[String]()

    ml += "top five recommened movies: " + myRecomendation.take(5).foldLeft(new StringJoiner(",")){ case (jnr,(mid, rating)) =>
      movies.get(mid) match {
        case Some(movie) => jnr.add(movie.mtitle +" "+ rating)
      }
    }.toString

    ml += "bottom five recommened movies: " +  myRecomendation.drop(myRecomendation.length - 6).foldLeft(new StringJoiner(",")){ case (jnr,(mid, rating)) =>
      movies.get(mid) match {
        case Some(movie) => jnr.add(movie.mtitle +" "+ rating)
      }
    }.toString + "\n"

    writeToFile("topBottom5RecommendMovies.txt", ml)

    println("================")


    val reviewsFlipped = users.flatMap(u => u.mRatings.values.map(ur => (ur.mname,ur.uid,ur.rating))).groupBy(_._1)

    val clo = reviewsFlipped.get("Clockwork Orange, A (1971)") match {
      case Some(x) => x
    }

    var mcor = reviewsFlipped.filterNot(it => it._1.equals("Clockwork Orange, A (1971)")).map(it => (it._1, pMovies(clo,it._2))).toList.sortBy(it => it._2).reverse
    ml = mutable.MutableList[String]()
    ml += "top five correlated recommened movies: " + mcor.take(5).foldLeft(new StringJoiner(",")){ case (jnr,(mid, rating)) =>

        jnr.add(mid+" "+rating+"\n")
    }.toString

    ml += "bottom five recommened movies: " +  mcor.drop(mcor.length - 6).foldLeft(new StringJoiner(",")){ case (jnr,(mid, rating)) =>
      jnr.add(mid+" "+rating+"\n")
    }.toString + "\n"

    writeToFile("ClockworkOrangetopBottom5RecommendMovies.txt", ml)

    println("================")


    mcor = reviewsFlipped.filterNot(it => it._1.equals("Jean de Florette (1986)")).map(it => (it._1, pMovies(clo,it._2))).toList.sortBy(it => it._2).reverse
    ml = mutable.MutableList[String]()
    ml += "top five correlated recommened movies: " + mcor.take(5).foldLeft(new StringJoiner(",")){ case (jnr,(mid, rating)) =>

      jnr.add(mid+" "+rating+"\n")
    }.toString

    ml += "bottom five recommened movies: " +  mcor.drop(mcor.length - 6).foldLeft(new StringJoiner(",")){ case (jnr,(mid, rating)) =>
      jnr.add(mid+" "+rating+"\n")
    }.toString + "\n"

    writeToFile("D3:TheMightyDuckstopBottom5RecommendMovies.txt", ml)

    println("================")




    //474|Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb
    //179|Clockwork Orange, A (1971)


  }
}
