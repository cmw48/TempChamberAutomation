

difference() {
union() {
// knob solids
translate([0, 0, 2]) cylinder(r=12, h=2, $fn=100);
translate([0, 0, 2]) cylinder(r=3, h=8, $fn=100);
translate([0, 0, -.5]) cylinder(r=2, h=3, $fn=100);    
}
// remove knob parts
union() {
rotate([90, 0, 0]) translate([0, 8.2, 0]) cylinder(r=.5, h=5) ;    
cylinder(r=1.5, h=12, $fn=100);
}
}


difference() {
translate([-30, -8, 0]) cube([70,130,1.5]);
translate([0, 0, -2]) cylinder(r=2.1, h=4, $fn=100);    
} 


difference(){
translate([-30, -8, 5]) cube([70,130,1.5]);
translate([0, 0, -5]) cylinder(r=3.1, h=12, $fn=100); 
}    

translate([-30, -8, -14]) cube([70,130,1.5]);

//rotate([90,0,180]) translate([-5.5, -6.2, 33]) 9g_motor();

//rotate([90,0,180]) translate([-5.5, -6.2, 83]) 9g_motor();

translate([-5.5, 0, -17]) 9g_motor();

translate([-5.5, 45, -17]) 9g_motor();

translate([-5.5, 90, -17]) 9g_motor();

module 9g_motor(){
	difference(){			
		union(){
			color("blue") cube([23,12.5,22], center=true);
			color("blue") translate([0,0,5]) cube([32,12,2], center=true);
			color("blue") translate([5.5,0,2.75]) cylinder(r=6, h=25.75, $fn=20, center=true);
			color("blue") translate([-.5,0,2.75]) cylinder(r=1, h=25.75, $fn=20, center=true);
			color("blue") translate([-1,0,2.75]) cube([5,5.6,24.5], center=true);		
			color("white") translate([5.5,0,3.65]) cylinder(r=2.35, h=29.25, $fn=20, center=true);				
		}
		translate([10,0,-11]) rotate([0,-30,0]) cube([8,13,4], center=true);
		for ( hole = [14,-14] ){
			translate([hole,0,5]) cylinder(r=2.2, h=4, $fn=20, center=true);
		}	
	}
}