package CassandraToS3

import org.apache.spark._
import com.datastax.spark.connector._
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types._
import org.apache.log4j.Logger
import org.apache.log4j.Level


object Transform{

  Logger.getLogger("org").setLevel(Level.OFF)
  Logger.getLogger("akka").setLevel(Level.OFF)

  val schema =
    StructType(
      StructField("id_sensor", StringType) ::
        StructField("id_campaign", IntegerType) ::
        StructField("vendor", StringType) ::
        StructField("mac_address", StringType) ::
        StructField("date_time_record", TimestampType) ::
        StructField("rssi", IntegerType) ::
        StructField("ssid", StringType) :: Nil
    )

  def main(args : Array[String]): Unit ={
    val conf = new SparkConf().setMaster("local[*]").setAppName("SparkZubatAnalytics").set("spark.cassandra.input.fetch.size_in_rows", "1000").set("spark.cassandra.connection.host", "34.196.59.158")
    val sc = SparkContext.getOrCreate(conf)
    val sqlContext = SparkSession.builder().enableHiveSupport().getOrCreate()
    sqlContext.sql("SET hive.exec.dynamic.partition=true")
    sqlContext.sql("SET hive.exec.dynamic.partition.mode=nonstrict")
    import sqlContext.implicits._

    val company = "claro"
//    val companyList = Array("semantix","bradesco","pernambucanas", "claro")
//    companyList.foreach(company => {
      val myTable = sc.cassandraTable(company,"measurement")
      val all_data_df = sqlContext.createDataFrame(myTable.map(
        r => org.apache.spark.sql.Row(
          r.columnValues(0).toString, // id_sensor
          r.columnValues(2).toString.toInt,  // id_campaign
          r.columnValues(3).toString, // vendor
          r.columnValues(4).toString, // mac_address
          new java.sql.Timestamp(r.columnValues(1).asInstanceOf[java.util.Date].getTime), // date_time_record
          r.columnValues(7).toString.toInt, // rssi
          r.columnValues(8).toString  // ssid
        )), schema)

      all_data_df.createOrReplaceTempView("partialData")
      //    all_data_df.createOrReplaceTempView("data")

//        sqlContext.sql("SELECT * FROM bradesco.notification").show()
      sqlContext.sql("INSERT INTO "+company+".measurement_prod PARTITION (id_sensor) SELECT id_campaign, vendor, mac_address, date_time_record, rssi, ssid, id_sensor FROM partialData")

//      println("MY PART HAS = "+part.count()+" ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
//      part.show(20)
//      sqlContext.sql("select * from bradesco.prod_measurement").show(20)
//      sqlContext.table("data").write.mode("append").format("parquet").saveAsTable("")
//      part.write.mode("append").format("parquet").saveAsTable("bradesco.measurement_raw")
      // all_data_df contains all data in a df (Check if amount will break spark)

      // Consume this data to Hive Table
//    })
  }
}
