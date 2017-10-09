var five = require("johnny-five"), 
    board = new five.Board();

board.on("ready", function() {

  var motor = new five.Motor({
    pins: { pwm: 5, pwm: 10 },
    register: { data: 0, clock: 2, latch: 7 },
    bits: { a: 2, b: 3 }
  });

  // Start the motor at maximum speed
  motor.forward(255);

});
