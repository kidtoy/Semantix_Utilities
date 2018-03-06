package StoreHive

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.streaming.StreamingContext
import LoadExternalData._
import org.apache.spark.storage.StorageLevel
import org.joda.time.{DateTime, Seconds}

object Main {

  case class InputRegister(sensor_id:String, date_time_sensor: java.sql.Timestamp, mac_address:String, prefix: String, rssi:Int, ssid: String, date_time_record: java.sql.Timestamp)

  def main(args: Array[String]): Unit = {
    @transient
    val conf = new SparkConf()
     .setMaster("local[4]")
     .setAppName("MqttToS3")
     .set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
     .set("spark.executor.memory","1g")
     .set("spark.driver.memory","1g")

    @transient
    val sc = SparkContext.getOrCreate(conf)
    sc.setLogLevel("ERROR")

    @transient
    val ssc = new StreamingContext(sc, org.apache.spark.streaming.Seconds(600))

    val topics = Array("df","dg","intelnuc","nuc")
    @transient
    val sqlContext = SparkSession.builder().getOrCreate()

    import sqlContext.implicits._

    val vendors = loadMacVendors(sqlContext)
    vendors.cache()

    val companyList = LoadExternalData.loadSensorsData(sqlContext)
    companyList.cache()

    /**
      * For each RDD received in the Stream, build the complete information,
      * i.e., fill vendor's name and campaign's ID.
      */
    Consumer.initMQTT(ssc,topics)
    val sensorDStreamClass = Consumer.MQTTRead()
    sensorDStreamClass.foreachRDD(foreachFunc = (rdd: RDD[Consumer.InputRegister]) => {

      val dt0 = new DateTime()

      val df: DataFrame = rdd.toDF("sensor_id","date_time_sensor","mac_address","prefix", "rssi", "ssid", "date_time_record").filter($"sensor_id" =!= "0")
      if(df.take(1).length > 0 ){

        val dfVendor = df.join(vendors, Seq("prefix"), "left_outer").na.fill(" ")
        val dfCompany = dfVendor.join(companyList, "sensor_id")
        val companies = dfCompany.select("company").distinct.collect.flatMap(_.toSeq).par
        val df_list = companies
          .map(company => dfCompany.where($"company" <=> company))
        df_list.foreach(ds => {

//           we use the company's name as keyspace
          val keyspace = ds.select($"company").first().getString(0).toLowerCase

              // select current information about sensors in this company
              try {
                println(keyspace + " count = " + ds.count())
                // prepare data frame to be inserted in the DB
                val dfToSave = ds.select($"sensor_id", $"deploy_id", $"vendor", $"mac_address", $"date_time_sensor", $"date_time_record", $"rssi", $"ssid")
                val path = "s3n://sense_testing/" + keyspace + "/measurement_raw/"+(System.currentTimeMillis / 1000)+"/"
                val rddToSave = dfToSave.rdd.map(x => x.mkString(",")).coalesce(1)
                rddToSave.saveAsTextFile(path)
//                rddToSave.first()
                rddToSave.unpersist()
              }
              catch {
                case exc: Throwable => println("Throwing something from storing to hive: " + keyspace)
                  exc.printStackTrace()
              }
        })
      }
      val dt1 = new DateTime()
      val diff = Seconds.secondsBetween(dt0, dt1).getSeconds()
      println(s"Tempo de resposta: $diff segundos")

    })
    // start streaming
    ssc.start()
    ssc.awaitTermination()
  }
}
