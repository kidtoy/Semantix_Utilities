package StoreHive

object DataCleaning {
  class DataCleaning extends Serializable {

    def dataCleaning(raw : Array[Byte]): Array[String]={

      // validate raw size
      if(raw.length != 17){
        print("raw string has less than 17 bytes. It has only " + raw.length + " bytes. ")
        raw.foreach(r=>{
          var str = ""
          for(pos <- 0 to 7){
            str = str + " " + ((r & (0x1 << pos)) >> pos)
          }
          println(str)
        })
        return null
      }

      val sensor_mac = new MACParse().parse(raw.slice(0,6))
      val device_mac = new MACParse().parse(raw.slice(10,16))
      val prefix_mac = device_mac.substring(0, 8)
      val date_time = new java.sql.Timestamp(new DateParse().parse(raw.slice(6, 10)).toLong).toString
      val rssi = "-"+((raw.slice(16,17).last >> 1) & 0x7F /* = 01111111 binary */).toString
      var ssid = ""
      if ((raw.slice(16,17).last & 0x1) == 0 ){
        ssid = " "
      }else{
        ssid = "Y"
      }
      Array(sensor_mac, date_time, device_mac, prefix_mac, rssi, ssid)
    }
  }
  class MACParse extends Serializable{

    /**
      * parse - this function parses the compacted MAC address
      * @param splitted - a byte Array represented an unsigned integer for each pair in the MAC address
      * @return the parsed string
      */
    def parse(splitted : Array[Byte]): String ={

      var fixedString = ""
      var value = 0

      for(x <- splitted){

        if(fixedString.length() > 0){
          // append ":"
          fixedString += ":"
        }

        // transform the 4 most significant bits into an hexa
        value = (15 << 4)
        value = (x & (15 << 4))
        value = (value >> 4)
        fixedString += value.toHexString

        // transform the 4 least significant bits into an hexa
        value = (x & 15)
        fixedString += value.toHexString
      }
      fixedString.toUpperCase
    }
  }


  class DateParse extends Serializable{

    /**
      * parse - this function parses the compacted date time transmitted by sensors
      * @param splitted - a byte array representing an unsigned integer with 32 bits with the difference
      *                 between the real timestamp and the time at 01-01-2017 00:00:00.
      * @return the parsed string
      */
    def parse(splitted : Array[Byte]): String ={

      var concatReadTime = 0.toLong

      // we read the byte array as a string: from the left to the right
      for(i_array <- 0 to 3){
        concatReadTime *= 256 // this multiplication guarantees the proper interpretation as a Long type
        var byteAsInt = 0
        // we read each bit in the byte from the left (most significant) to the right
        for(i_byte <- 7 to 0 by -1){
          val bit = splitted(i_array) & (0x1 << i_byte)
          byteAsInt += bit // this sum guarantees the proper cast from byte to int
        }
        concatReadTime += byteAsInt
      }
      val response = new org.joda.time.DateTime("2016-12-31T22:00:00").getMillis + (concatReadTime.toLong * 1000)
      response.toString
    }
  }
}
