var five = require("johnny-five");
var board = new five.Board();

board.on("ready", function() {

console.log("Ready.");

var stepper = new five.Stepper({
  type: five.Stepper.TYPE.DRIVER,
  stepsPerRev: 200,
  pins: {
    step:11, 
    dir: 13
  }
});

stepper.rpm(10).ccw().step(5, function() {
  console.log("Done moving 5 steps ccw.");
});


});
