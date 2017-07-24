// tempmonitor.js
// controller.js
const mqtt = require('mqtt')

var client  = mqtt.connect('mqtt://mqtt.opensensors.io',{
  username: 'wickeddevice',
  password: 'mXtsGZB5',
  clientId: '2940'

});

var currentTemp = ''
var connected = false
var topic = '/orgs/wd/aqe/temperature/'
var eggserial = 'egg00802d94e5080102'
var topicString = topic + eggserial
console.log('topic string %s', topicString)



client.on('message', function (topic, message) {
  // message is Buffer
  console.log(message.toString());
  client.end();
});





//mqtt.Client#subscribe(topic/topic array/topic object, [options], [callback])
//topic = "/orgs/wd/aqe/temperature/"
//eggserial = "egg00802d94e5080102"



client.on('connect', () => {
  client.subscribe(topicString);
})

client.on('message', (topic, message) => {
  switch (topic) {
    case 'garage/connected':
      return handleGarageConnected(message)
    case 'garage/state':
      return handleGarageState(message)
  }
  console.log('No handler for topic %s', topic)
})

function handleGarageConnected (message) {
  console.log('garage connected status %s', message)
  connected = (message.toString() === 'true')
}

function handleGarageState (message) {
  garageState = message
  console.log('garage state update to %s', message)
}

function openGarageDoor () {
  // can only open door if we're connected to mqtt and door isn't already open
  if (connected && garageState !== 'open') {
    // Ask the door to open
    client.publish('garage/open', 'true')
  }
}

function closeGarageDoor () {
  // can only close door if we're connected to mqtt and door isn't already closed
  if (connected && garageState !== 'closed') {
    // Ask the door to close
    client.publish('garage/close', 'true')
  }
}

// --- For Demo Purposes Only ----//

// simulate opening garage door
setTimeout(() => {
  console.log('open door')
  openGarageDoor()
}, 5000)

// simulate closing garage door
setTimeout(() => {
  console.log('close door')
  closeGarageDoor()
}, 20000)

**/
