 //machine parts
//backplane
module thermotron(){
translate([-30, -8, 19]) color([.71,.65,.65]) cube([115,130,1.5]);

//potentiometer
translate([0, 0, 3]) color([.8,.65,.65]) cylinder(r=3.17, h=16.8, $fn=100);
translate([0,0,15.1]) color([.8,.65,.65])cylinder(r=7, h=4.7, $fn=100);

//heat cool switch
translate([57, 51, -2]) color([.8,.65,.65]) cylinder(r=3.17, h=20.85, $fn=100);
translate([57, 51, 14.85]) color([.8,.65,.65]) cylinder(r=7, h=4.7, $fn=100);

//set point switch
translate([0, 102, 3]) color([.8,.65,.65]) cylinder(r=1.17, h=14.45, $fn=100);
translate([0, 102, 15.5]) color([.8,.65,.65]) cylinder(r=7, h=3.8, $fn=100);
    
}

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

module knobadd(){
     union() {
    // knob solids

      translate([0, 0, 2]) cylinder(r=15, h=2, $fn=100);
      translate([0, 0, 2]) cylinder(r=4.5, h=10, $fn=100);
      translate([0, 0, -1.1]) cylinder(r=3.5, h=3.5, $fn=100);    
  }   
}    

module knobsubtract(){
// remove knob parts
    union() {
      translate([0, 0, 3]) color([.8,.65,.65]) cylinder(r=3.17, h=16.8, $fn=100);
      rotate([90, 0, 0]) translate([0, 9.2, 0]) cylinder(r=.5, h=5) ;    
    translate([hole,0,5]) cylinder(r=2.2, h=4, $fn=20, center=true);
     for ( i = [0 : 15] ){
       rotate( i * 360 / 15, [1, 0, 90])
       translate([0, 15, 0])
       cylinder(r = 1.5, h=5, $fn=25);
     }
   }
}

module renderknob(){
  difference() {
    knobadd();
    knobsubtract();
 }
}




module renderservos(){
  translate([-5.5, 0, -12]) scale([1.02,1.02,1.02]) 9g_motor();

  translate([51, 38, -12]) scale([1.02,1.02,1.02])9g_motor();

  translate([-5.5, 92, -12]) 9g_motor();
}

module platebottom() {
    difference(){
      translate([-30, -11, 5]) cube([115,85,1.5]);
      translate([0, 0, 3]) cylinder(r=4.85, h=4, $fn=100); 
 }    
}

module platemiddle() {
  difference() {
    translate([-30, -11, 0]) cube([115,85
     ,1.5]);
    translate([0, 0, -2]) cylinder(r=3.75, h=4, $fn=100);    
}   
}

module platetop() {
    translate([-30, -11, -14]) cube([115,85,1.5]);
}


module plateadd(){
   //platetop();
   platemiddle();
   //platebottom();
}    


module platesubtract() {
    union() {
        renderservos();
        translate([40, 46, -10]) color([.8,.65,.65]) cube([35, 11, 25]);
        translate([-13, 97, -10]) color([.8,.65,.65]) cube([25, 10, 25]);    
        // screwholes
        translate([-24, 68, -20]) color([.8,.65,.65]) cylinder(r=1.6, h=60, $fn=100);
        translate([-24, -5, -20]) color([.8,.65,.65]) cylinder(r=1.6, h=60, $fn=100);
        translate([-24, 31, -20]) color([.8,.65,.65]) cylinder(r=1.6, h=60, $fn=100);    
        //    
        translate([78, 68, -20]) color([.8,.65,.65])
    cylinder(r=1.6, h=60, $fn=100);   
        translate([78, -5, -20]) color([.8,.65,.65]) cylinder(r=1.6, h=60, $fn=100);  
        translate([78, 31, -20]) color([.8,.65,.65]) cylinder(r=1.6, h=60, $fn=100); 
        translate([28, 68, -20]) color([.8,.65,.65])
    cylinder(r=1.6, h=60, $fn=100);     
        translate([28, -5, -20]) color([.8,.65,.65])
    cylinder(r=1.6, h=60, $fn=100); 
        translate([28, 31, -20]) color([.8,.65,.65])
    cylinder(r=1.6, h=60, $fn=100);      
     
///
        translate([37, 38, -20]) color([.8,.65,.65])
    cylinder(r=1.6, h=10, $fn=100);   
        translate([65, 38, -20]) color([.8,.65,.65])
    cylinder(r=1.6, h=10, $fn=100);      
    
        translate([8, 0, -20]) color([.8,.65,.65])
    cylinder(r=1.6, h=10, $fn=100);   
        translate([-20, 0, -20]) color([.8,.65,.65])
    cylinder(r=1.6, h=10, $fn=100);    
        
    }    
}

module plates() {
  difference() {
    plateadd();
    platesubtract();
  }      
};

//thermotron();
//renderknob();
//renderservos();
projection() {
plates();
}
