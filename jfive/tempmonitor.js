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

function handleTestRunning (message) {
  console.log('Test in progress status %s', message)
  connected = (message.toString() === 'true')
}

function handleStableState (message) {
  stableState = message
  console.log('stable state update to %s', message)
}

function seekTemperature () {
  // if unstable, we are trying to reach a temp
  if (connected && stableState !== 'stable') {
    // what is the currentTemp vs targetTemp
    // code to monitor for stability
  }
}

function holdTemperature () {
  // if stable, we need to stay that way for one hour
  if (connected && stableState !== 'unstable') {
    // how much time has elapsed since stability lockup
    // code to count off one hour
  }
}

/**

// simulate opening garage door
setTimeout(() => {
  console.log('pause until next temp message')
  getTemp()
}, 5000)

// simulate closing garage door
setTimeout(() => {
  console.log('count off one hour from stability lockup')
  holdTime()
}, 3600000)

**/
