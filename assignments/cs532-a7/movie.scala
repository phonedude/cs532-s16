package jberlin


object movie {
  implicit def arrTom(ar:(String, String)): movie  = new movie(ar._1.toInt,ar._2)
}

class movie(val mid: Int, val mtitle: String) {
  override def toString = s"movie($mid, $mtitle)"
}
