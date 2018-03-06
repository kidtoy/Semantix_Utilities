package ExportHiveToCassandra

import org.apache.spark._
import com.datastax.spark.connector._
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.log4j.Logger
import org.apache.log4j.Level

object Transform{



  case class  cassandraR(id_sensor:String, date_time:java.sql.Timestamp, id_campaign:Int, vendor:String, mac_address:String, distance:Int, date_time_recorded:java.sql.Timestamp, rssi:Int, ssid: String)

  def main(args : Array[String]): Unit ={
    val conf = new SparkConf().setMaster("local[*]").setAppName("SparkRetrieveData").set("spark.cassandra.input.fetch.size_in_rows", "1000").set("spark.cassandra.connection.host", "34.196.59.158")
    val sc = SparkContext.getOrCreate(conf)
    val sqlContext = SparkSession.builder().enableHiveSupport().getOrCreate()
    Logger.getLogger("org").setLevel(Level.OFF)
    Logger.getLogger("akka").setLevel(Level.OFF)
    import sqlContext.implicits._

    val company = "pernambucanas"
//    val companyList = Array("bradesco","pernambucanas", "claro")
//    companyList.foreach(company => {
      val df = sqlContext.sql("SELECT * FROM "+company+".measurement_prod where  date_time_record > '2018-02-17 15:00:01' and date_time_record < '2018-02-19 06:00:00'")
//      df.show
//            println(df.first())
      val df2 = df.withColumnRenamed("deploy_id", "id_campaign")
        .withColumnRenamed("date_time_sensor", "date_time")
        .withColumnRenamed("date_time_record", "date_time_recorded")
        .withColumnRenamed("sensor_id","id_sensor")
    .withColumn("distance", lit(1))
        .select("id_sensor","date_time","id_campaign","vendor","mac_address","distance","date_time_recorded","rssi","ssid")

      df2.show(5)
//      println(df2.rdd.first())
      df2.rdd.map(r=> cassandraR(r.get(0).toString,new java.sql.Timestamp(r.get(1).asInstanceOf[java.util.Date].getTime),r.get(2).toString.toInt,r.get(3).toString,r.get(4).toString,r.get(5).toString.toInt,new java.sql.Timestamp(r.get(6).asInstanceOf[java.util.Date].getTime),r.get(7).toString.toInt,r.get(8).toString)).saveToCassandra(company,"measurement")
//      df2.write.mode("append").format("org.apache.spark.sql.cassandra").options(Map("keyspace" -> company, "table" -> "measurement")).save()
//    })
  }
}
