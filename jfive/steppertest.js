var five = require("johnny-five");
var board = new five.Board({debug: true});

board.on("ready", function() {
  var k = 0;
  var stepper = new five.Stepper({
    type: five.Stepper.TYPE.DRIVER,
    stepsPerRev: 200,
    pins: [11, 13]
  });

  stepper.rpm(10).ccw().step(200, function() {
    console.log("done");
  });
});
