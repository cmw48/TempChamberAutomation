// tempmonitor.js

//const {promisify} = require('util');
const mqtt = require('mqtt');
var typeOf = require('typeof');

//const getTemp = promisify(getEggTemp());

var currentTemp = '';
var connected = false;
var topic = '/orgs/wd/aqe/temperature/';
var eggserial = 'egg00802294f10b0142';
var topicString = topic + eggserial;
console.log('topic string %s', topicString);
var msgcount = 0;

var targetTempArray = [0,15,25,30,35,40];
var recentTempArray=[];
var tempRecordArray=[];
var deltasArray=[];



var client  = mqtt.connect('mqtt://mqtt.opensensors.io',{
  username: 'wickeddevice',
  password: 'mXtsGZB5',
  clientId: '2940'

});
if (process.platform === "win32") {
  var rl = require("readline").createInterface({
    input: process.stdin,
    output: process.stdout
  });

  rl.on("SIGINT", function () {
    process.emit("SIGINT");
  });
}


client.on('message', function (topic, message) {
  // message is Buffer
  // write entire message to console
  console.log(JSON.parse(message));
  var targetTemp = 0;
  var tempRightNow = getEggTemp(message, targetTemp);
  console.log('right now the egg temp is %s', tempRightNow);
  msgcount++;
  console.log(JSON.parse(message));
   console.log('%s messages', msgcount);
  //let json = JSON.parse(message);
  //console.log(json['converted-value']);
  //client.end();
});


client.on('connect', () => {
  client.subscribe(topicString);
  var msgcount = 0;
});

function getEggTemp (message, targetTemp) {

  let json = JSON.parse(message);
  var currentTemp = json['converted-value'];

  console.log('the egg temp is %s', currentTemp );
  console.log('the target temp is %s', targetTemp );
  console.log('for a difference of %s', currentTemp-targetTemp )
  //connected = (message.toString() === 'true')
  return currentTemp;
};

/*
console.log('For loop should give us five messages');
for(var i = 0; i < 5; i++) {

 console.log(msgcount);
 client.end();
}
*/
/**
getTemp(message, targetTemp)
  .then((text) => {
      console.log('made it:', currentTemp);
  })
  .catch((err) => {
      console.log('ERROR:', err);
  });
  **/

//function
//getEggTemp();

//mqtt.Client#subscribe(topic/topic array/topic object, [options], [callback])
//topic = "/orgs/wd/aqe/temperature/"
//eggserial = "egg00802d94e5080102"




/**Example code
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


process.on("SIGINT", function () {
  //graceful shutdown
  console.log('received CTRL-C SIGINT, shutting down...');
  client.end();
  console.log('closed connection to client.');
  process.exit();
});
