package jberlin

object urating{
  implicit def arrToUr(ar:Array[String]): urating  =
    new urating(ar(0).toInt,ar(1).toInt,ar(2).toInt,ar(3))
  implicit def urToI(ur:urating): Number = ur.rating
}

class urating(val uid: Int, val itemId: Int, val rating: Int, val tstamp:String,var mname:String =null) {
  override def toString = s"urating($uid, $itemId, $mname, $rating)"

  def canEqual(other: Any): Boolean = other.isInstanceOf[urating]

  override def equals(other: Any): Boolean = other match {
    case that: urating =>
      (that canEqual this) &&
        itemId == that.itemId &&
        mname == that.mname
    case _ => false
  }

  override def hashCode(): Int = {
    val state = Seq(uid, itemId, rating, tstamp, mname)
    state.map(_.hashCode()).foldLeft(0)((a, b) => 31 * a + b)
  }
}
