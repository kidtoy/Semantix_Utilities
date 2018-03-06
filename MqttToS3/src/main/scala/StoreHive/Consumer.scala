package StoreHive

import org.apache.spark.storage.StorageLevel
import org.apache.spark.streaming.dstream.{DStream, ReceiverInputDStream}
import org.apache.spark.streaming.mqtt.MQTTUtils
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.{SparkConf, SparkContext}
import org.eclipse.paho.client.mqttv3.MqttConnectOptions
import DataCleaning._
import org.joda.time.DateTime


object Consumer{

  case class InputRegister(sensor_id:String, date_time_sensor: java.sql.Timestamp, mac_address:String, prefix: String, rssi:Int, ssid: String, date_time_record: java.sql.Timestamp)

  @transient
  var lines :ReceiverInputDStream[(String,Array[Byte])] = null

  def initMQTT(ssc : StreamingContext, topics: Array[String]): Unit ={
    this.lines = MQTTUtils.createPairedByteArrayStream(
      ssc,
      "tcp://34.196.59.158:1883",
      topics,
      StorageLevel.MEMORY_ONLY,
      Option("SparkStorage"),
      Option("spark"), Some("123456"),
      Option(true),
      Option(0),
      Option(MqttConnectOptions.CONNECTION_TIMEOUT_DEFAULT),
      Option(60),
      Option(MqttConnectOptions.MQTT_VERSION_3_1_1))
  }

  def MQTTRead(): DStream[InputRegister] ={

    @transient
    val sensorDStream: DStream[InputRegister] = lines.flatMap(value => {
      val partedData = value._2.grouped(17).toSeq
      partedData.map(data => {
        val clean = new DataCleaning().dataCleaning(data)
        val date_time = new DateTime()
        try {
          InputRegister(
            clean(0).toUpperCase(), // id_sensor
              java.sql.Timestamp.valueOf(clean(1)), // date_time
              clean(2).toUpperCase(), // MAC
              clean(3), //MAC prefix
              clean(4).toInt, // rssi
              clean(5), //ssid
              new java.sql.Timestamp(date_time.toDate.getTime)// date_time recorded
            )
          }
        catch {
          case exc: Exception =>
            println("I Dislike this string")
            clean.foreach(r => println(r))
            InputRegister(
              "0", // id_sensor
              java.sql.Timestamp.valueOf("2000-01-01 00:00:01.000"), // date_time
              "0", // MAC
              "0", //MAC prefix
              0, // rssi
              "0", //ssid
              new java.sql.Timestamp(date_time.toDate.getTime)// date_time recorded
            ) // Caso haja dados corrompidos, Retornar no lugar um valor 0
        }
      })
    })
    sensorDStream
   }
}
