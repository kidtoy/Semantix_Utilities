'use strict';

const redis = require('redis')
const request = require('request')
const db = redis.createClient({
  host: '34.228.20.244',
  port: '6379'
})

exports.handler = (event, context) => {
  const mac = event.mac_address
  const agencia = event.branch
  const section = event.section
  let merge = event.person
  let postData = event
  var options = {
    method: 'post',
    body: postData, // Javascript object
    json: true, // Use,If you are sending JSON data
    url: 'https://semantixsense.com.br:8880/notification/api/manager',
    headers: {
      'Content-Type': 'application/json'
    }
  }
  console.log(merge)
  db.select(4, function (err, res) {
    if (err) {
      console.log('Wrong Database')
    }
    db.get(merge, function (err, reply) {
      if (err) {
        console.log('something unexpected happened')
      }
      if (reply == null) {
        // process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0' // Ignore Certificate errors
        request(options, function (err, res, body) {
          if (err) {
            console.log('Error :', err)
          }
          console.log('Received Message: ', body)
          db.set(merge, section, 'EX', 15 * 60, function (err, res) {
            if (err) {
              console.log(null, 'SOMETHING GOT WRONG')
            } else {
              console.log('Done')
              context.done(null, 'success')
            }
          })
        })
      } else {
        console.log(`Already exists person: ${reply}`)
        db.set(merge, section, 'EX', 15 * 60, function (err, res) {
          if (err) {
            console.log(null, 'SOMETHING GOT WRONG')
          } else {
            console.log('Done')
            context.done(null, 'success')
          }
        })
      }
    })
  })
}
