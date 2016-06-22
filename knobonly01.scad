difference() {
union() {
// knob solids

translate([0, 0, 2]) cylinder(r=15, h=2, $fn=100);
translate([0, 0, 2]) cylinder(r=4.5, h=10, $fn=100);
translate([0, 0, -.5]) cylinder(r=2, h=3, $fn=100);    
}
// remove knob parts
union() {

translate([0, 0, 3]) cylinder(r=3.17, h=16.8, $fn=100);
translate([0,0,15.1]) cylinder(r=7, h=4.7, $fn=100);

    
rotate([90, 0, 0]) translate([0, 9.2, 0]) cylinder(r=.5, h=5) ;    
    
for ( i = [0 : 15] )
{
rotate( i * 360 / 15
    , [1, 0, 90])
translate([0, 15, 0])
cylinder(r = 1.5, h=5, $fn=25);
}
    
}
//}
