# TempChamberAutomation

Prototypical code for Temperature Chamber automation control.  Uses Paho python library to 
subscribe to egg temp readings and make decisions about when to modify temp chamber settings.

Mission: read a temperature data point, and decide whether to 
+ wait, and count a clock
+ turn a knob
+ flip a switch

<ol>
<li> [userio] enter an egg serial number
<li> [preset]  switch to COOL, set temp to -20C
<li> start "outer loop" run elapsed-time timer 
<li> subscribe to egg data stream
<li> query sensor data at opensensors.io (using MQTT messages)
<li> gather a list of the last ten temperatures
<li> determine the "slope" (rate of change, delta of deltas, whateveryouwannacallit)
<li> are we stable?  
<ul><li> No? keep going, and run a clock to say how long we've been unstable
<li>Yes? reset the "stable since 00:XX:XX" clock and run for an hour.
</ul>
<li> after you have been stable for an hour, do some shtuff:
<ul><li> increment the step counter to say we are coing to the next level
<li> turn a knob to turn the temp up to the next temperature step
<li> flip a switch from COOL to HEAT at one point (when we cross the room temp line)
</ul>
<li> detect that the temp is changing, and drop out of "stability lock"     
<li> do this like 5 more times at different temps.  
<li> when the last outer loop is done, flip the switch to the middle position to shut that f**ker off.
<li> check to see if it shut off (not heating or cooling any more)
</ol>

NOTE: We don't store any egg temperature data-- it's all saved separately in the cloud.  We are just looking at the temp inside the box (as measured by the egg) and making decisions about when to turn the knob, and when to flip the switch.

TODO: 
-  non-blocking threaded receipt and interpretation of messages (waiting for a message does not block other code-- i.e. elapsed time clocks)
- fix reconnect problem: 
  - we get about one temp message every five or six seconds
  - occasionally we go 15 sec without a message, then we get three all at once, then maybe one more, then nothing.
  - "if you don't get a message after 30 seconds have elapsed, try to reconnect."

HARD PART: 
- mechanical control requires arduino on a pi. 
- turn knob with a servo? stepper motor?  simple is better.
- flip switch with a SECOND servo means you can't just get away with the RaspPi, now you need the Arduino, too.   Maybe figure out how to do the whole thing with a wi-fi Arduino?

BONUS: 
- tell me what the temp is in the egg, and possibly track multiple eggs to 
- display times (what's the elapsed time?, how long until the next step?, when will this be over??)
- maybe an LCD display
