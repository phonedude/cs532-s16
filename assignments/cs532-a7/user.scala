package jberlin

object user{
  implicit def arrToU(ar:Array[String]): user =
    new user(ar(0).toInt,ar(1).toInt,ar(2).charAt(0),ar(3),ar(4))
}
class user(val id: Int, val age: Int, val  gender:Char,val  job:String, val zcode:String,
           var mRatings: Map[Int,urating] = Map[Int,urating](),var corToMe: Double = 0.0) {
//  def ratingMean = mRatings.foldLeft(0.0)((acum,ur)=>acum + ur.rating) / mRatings.length
//  def ratedMovie(id: Int) =
//    mRatings.count(ur => ur.itemId == id) == 1
  override def toString = s"user($id, $age, $gender, $job)"
}


