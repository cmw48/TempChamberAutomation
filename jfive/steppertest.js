var five = require("johnny-five");
var board = new five.Board({debug: true});

board.on("ready", function() {
  var k = 0;
  var stepper = new five.Stepper({
    type: five.Stepper.TYPE.DRIVER,
    stepsPerRev: 200,
    pins: [25, 15]
  });

  stepper.rpm(10).cw().step(2000, function() {
    console.log("done");
  });
});
