package StoreHive

import org.apache.spark.sql.{DataFrame, SparkSession}

object LoadExternalData {
  def loadMacVendors(sqlContext: SparkSession): DataFrame = {
    sqlContext.read.format("jdbc")
      .option("url", "jdbc:mysql://sensedb.cenacuetgbbz.us-east-1.rds.amazonaws.com/sense")
      .option("port", "3306")
      .option("driver", "com.mysql.cj.jdbc.Driver")
      .option("dbtable", "vendor_mac")
      .option("user", "lambda")
      .option("password", "LAMBDA@112358")
      .load()
      .withColumnRenamed("mac_address","prefix")
  }

  def loadSensorsData(sqlContext: SparkSession): DataFrame = {
    sqlContext.read.format("jdbc")
      .option("url", "jdbc:mysql://sensedb.cenacuetgbbz.us-east-1.rds.amazonaws.com/sense")
      .option("port", "3306")
      .option("driver", "com.mysql.cj.jdbc.Driver")
      .option("dbtable", "view_sensor_sense")
      .option("user", "lambda")
      .option("password", "LAMBDA@112358")
      .load()
  }
}
