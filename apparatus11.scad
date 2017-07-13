 //machine parts
//backplane
module thermotron(){
translate([-45, -50, 19]) color([.71,.65,.65]) cube([150,160,1.5]);

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
//adjusted z height of servo to make holes
module 9g_motor(){
	difference(){			
		union(){
			color("blue") translate([0,0,-3]) cube([23,12.5,28], center=true);
			color("blue") translate([0,0,5]) cube([32,12,2], center=true);
			color("blue") translate([5.5,0,2.75]) cylinder(r=6, h=25.75, $fn=20, center=true);
			color("blue") translate([-.5,0,2.75]) cylinder(r=1, h=25.75, $fn=20, center=true);
			color("blue") translate([-1,0,2.75]) cube([5,5.6,24.5], center=true);		
			color("white") translate([5.5,0,3.65]) cylinder(r=2.35, h=29.25, $fn=20, center=true);		
		}
		//translate([10,0,-11]) rotate([0,-30,0]) cube([8,13,4], center=true);
		for ( hole = [14,-14] ){
		translate([hole,0,5]) cylinder(r=2.2, h=4, $fn=20, center=true);
		}	
	}
}


/**
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

**/


module renderservos(){
  //comment servo if using stepper for potentiometer adjustment  
  //translate([-5.5, 0, -12]) scale([1.02,1.02,1.02]) 9g_motor();
 // added -10 z ofs for stepper placement (was -12)
  translate([51, 37, -22]) scale([1.02,1.02,1.02])9g_motor();

  translate([-5.5, 88, -22]) 9g_motor();
}

module rendersteppers(){
  translate([0, 0, -68]) scale([1.02,1.02,1.02]) nema17();

  //translate([51, 38, -12]) scale([1.02,1.02,1.02])9g_motor();

  //translate([-5.5, 92, -12]) 9g_motor();
}

//coupler offsets 0,-35,-37.2
module rendercoupler() {
     rotate([90, 0, 0]) translate([0, -5, 0]) scale([1.02,1.02,1.02]) coupler(); 
};

// added 12 to account for grubscrews
module platebottom() {
    difference(){
      translate([-30, -35, 5]) cube([115,151,1.5]);
      translate([0, 0, 3]) cylinder(r=4.85, h=4, $fn=100); 
 }    
}
 // added -14 z ofs for stepper placement (was -12)
module platemiddle() {
  difference() {
    translate([-30, -35, -9]) cube([115,150
     ,1.5]);
    translate([0, 0, -16]) cylinder(r=3.75, h=4, $fn=100);    
}   
}

//added -10
module platetop() {
    translate([-30, -35, -15]) cube([150,150,1.5]);
}

//added to hold servos and guide coupler
module platetiptop() {
    translate([-30, -35, -33]) cube([150,150,1.5]);
}


module plateadd(){
   platetiptop(); 
   platetop();
   platemiddle();
   platebottom();
}    


module platesubtract() {
    union() {
    renderservos();
    rendersteppers();
    rendercoupler();    
        translate([40, 46, -40]) color([.8,.65,.65]) cube([35, 11, 50]);
        translate([-13, 97, -40]) color([.8,.65,.65]) cube([25, 10, 50]);    
        // screwholes
       //lefttop
        translate([-24, 110, -60]) color([.8,.65,.65]) cylinder(r=1.6, h=100, $fn=100);
       //righttop 
        translate([-24, -30, -60]) color([.8,.65,.65]) cylinder(r=1.6, h=100, $fn=100);
        //middletop
        translate([-24, 31, -60]) color([.8,.65,.65]) cylinder(r=1.6, h=100, $fn=100);    
        //leftcenter
        translate([78, 110, -60]) color([.8,.65,.65]) cylinder(r=1.6, h=100, $fn=100);   
        //rightcenter
        translate([78, -30, -60]) color([.8,.65,.65]) cylinder(r=1.6, h=100, $fn=100);  
        //midllecenter
        translate([78, 31, -60]) color([.8,.65,.65]) cylinder(r=1.6, h=100, $fn=100); 
        
        //leftbottom
        translate([28, 110, -60]) color([.8,.65,.65])
    cylinder(r=1.6, h=100, $fn=100);     
        translate([28, -30, -60]) color([.8,.65,.65])
    cylinder(r=1.6, h=100, $fn=100); 
        translate([28, 31, -60]) color([.8,.65,.65])
    cylinder(r=1.6, h=100, $fn=100);      

        //leftrockbottom
        translate([113, 110, -60]) color([.8,.65,.65])
    cylinder(r=1.6, h=100, $fn=100);     
        translate([113, -30, -60]) color([.8,.65,.65])
    cylinder(r=1.6, h=100, $fn=100); 
        translate([113, 31, -60]) color([.8,.65,.65])
    cylinder(r=1.6, h=100, $fn=100);  
    
//TODOchange servoscrew diameter    
//servo2 lower
        translate([37, 37, -20]) color([.8,.65,.65])
    cylinder(r=1.6, h=20, $fn=100);  
//servo2 upper    
        translate([65, 37, -20]) color([.8,.65,.65])
    cylinder(r=1.6, h=20, $fn=100);      
  
//servo1 upper and lower
       translate([8, 0, -20]) color([.8,.65,.65]) cylinder(r=1.6, h=20, $fn=100);   
       translate([-20, 0, -20]) color([.8,.65,.65]) cylinder(r=1.6, h=20, $fn=100);    
//servo3 upper and lower
       translate([-20, 88, -20]) color([.8,.65,.65]) cylinder(r=1.6, h=20, $fn=100);   
       translate([8, 88, -20]) color([.8,.65,.65]) cylinder(r=1.6, h=20, $fn=100);           
    }    
}


module nema17() {
    //Quick design of a NEMA 17 (SM-42BYG011-25) motor
    //adjusted to subtract geometry
debug = 0;

motor_height = 34.0;

cylinderheight = 4.59;
shaftlength = 21.8;  //measured from top of cylinder


keyheight = 3.3;
keywidth = 3.24;
keyfromcenter = 1.52;



if(debug == 0){
	//difference(){
//motor
		union(){
			translate([0,0,motor_height/2]){
				intersection(){
					cube([42.3,42.3,motor_height], center = true);
					rotate([0,0,45]) translate([0,0,-1]) cube([74.3*sin(45), 73.3*sin(45) ,motor_height+2], center = true);
				}
			}
            //lower cylinder
			translate([0, 0, motor_height]) cylinder(h=cylinderheight, r=11, $fn=24);
            difference() {
              //shaft
			  translate([0, 0, motor_height+cylinderheight]) cylinder(h=shaftlength, r=2.5, $fn=24);
              //key
              rotate([0,0,45]) translate([keyfromcenter, -keywidth, motor_height+cylinderheight+keyheight]) cube([2*keywidth,2*keywidth,shaftlength]);
            }    
		}
//screw holes
		for(i=[0:3]){
				rotate([0, 0, 90*i])translate([15.5, 15.5, motor_height]) cylinder(h=5, r=1.5, $fn=24);
			}
	//}
}
 
};

// modified outershaft radius
module coupler() {
    spaceBetween = 2.5;

inShaft = 20;
inShaftDiameter = 5.4; //5

outShaft = 13;
outShaftDiameter = 6.7; //6.3

inShaftLength = inShaft + spaceBetween;
outShaftLength = outShaft + spaceBetween;

inGrub = 1;
outGrub = 1;
grubDiameter = 3; 
grubHeadDiameter =5.9;
grubScrewHeight = 8.7;



inKey = 1;
inKeyDiameter = 4.5;
inKeyLength = 15;

// later, change these to be conditional
outKey = 0;
outKeyDiameter = 6.3;
outKeyLength = outShaftLength;

couplerBoltShaftLength = 8.7;
//couplerBoltShaftLength = 21.5;
couplerBoltHeadLength = 2.5;
couplerBoltShaftDiameter = 3;
couplerBoltHeadDiameter = 5.9;
couplerNutDiameter = 5.9; //5.5
couplerNutHeight = 2.8;  //2.3

outerCylinderDiameter = outShaftDiameter+17;
outerCylinderLength = (inShaftLength + outShaftLength);
// top level geometry goes here
difference() {
  allAdd();  
  allSubtract();  


}
// 
module allAdd() {
    translate ([0,((outerCylinderLength-7)/2),0]) rotate ([90,0,0]) cylinder(h=(outerCylinderLength), r=outerCylinderDiameter/2);
     translate ([0,-inShaft+3,0]) rotate ([90,0,0]) renderknob();           
}


// draw input side subtractions
//commented slots for subraction from apparatus
module allSubtract() {
     shaftSubtract();
     //grubSubtract();
     //nutSlotSubtract();

}
module shaftSubtract() {

translate ([0,0,0]) rotate ([90,0,0]) cylinder(h=inShaftLength, r=inShaftDiameter/2);

translate ([0,outShaftLength,0]) rotate ([90,0,0]) cylinder(h=outShaftLength, r=outShaftDiameter/2);    
    
}

module grubSubtract() {
//inKey grub
translate ([0,-(inKeyLength/2),-(inShaftDiameter-inKeyDiameter)]) rotate ([0,0,0]) cylinder(h=grubScrewHeight, r=grubDiameter/2);
    
//outKey grub
translate ([0,(outKeyLength/2),-(outShaftDiameter-outKeyDiameter)]) rotate ([0,0,0]) cylinder(h=grubScrewHeight, r=grubDiameter/2);

//inKey grubhead
translate ([0,-(inKeyLength/2),(-(inShaftDiameter-inKeyDiameter)*2)+grubScrewHeight]) rotate ([0,0,0]) cylinder(h=outerCylinderDiameter+3, r=grubHeadDiameter/2);
    
//inKey grubhead
translate ([0,(outKeyLength/2),(-(outShaftDiameter-outKeyDiameter)*2)+grubScrewHeight]) rotate ([0,0,0]) cylinder(h=outerCylinderDiameter+3, r=grubHeadDiameter/2);
}

module nutSlotSubtract() {

translate ([-couplerNutDiameter/2,outShaftLength/2-couplerNutDiameter,(grubScrewHeight/2)]) rotate ([0,0,0]) cube([couplerNutDiameter, outShaftLength/2+couplerNutDiameter, couplerNutHeight]);
    
translate ([-couplerNutDiameter/2,-(inShaftLength),(grubScrewHeight/2)]) rotate ([0,0,0]) cube([couplerNutDiameter, inShaftLength/2+(couplerNutDiameter)+(inShaftLength-inKeyLength), couplerNutHeight]);    
}

// draw output side geometry

// draw output side subtractions


// draw grub screw subtractions
// includes screwhole depth and linear placement
// as well as captive nut subtractions


  module knobadd(){
     union() {
    // knob solids

      translate([0, 0, 2]) cylinder(r=35, h=2, $fn=100);
      //translate([0, 0, 2]) cylinder(r=4.5, h=10, $fn=100);
      //translate([0, 0, -1.1]) cylinder(r=3.5, h=3.5, $fn=100);    
  }   
}    

module knobsubtract(){

// remove knob parts
    union() {
      translate([0, 0, 3]) color([.8,.65,.65]) cylinder(r=3.17, h=16.8, $fn=100);
      rotate([90, 0, 0]) translate([0, 9.2, 0]) cylinder(r=.5, h=5) ;    
    translate([0,0,5]) cylinder(r=2.2, h=4, $fn=20, center=true);
     for ( i = [0 : 15] ){
       rotate( i * 360 / 15, [1, 0, 90])
       translate([0, 35, 0])
       cylinder(r = 3, h=5, $fn=25);
     }
   }
}

module renderknob(){
  difference() {
    knobadd();
    knobsubtract();
 }
}







};


module plates() {
  difference() {
    plateadd();
    platesubtract();
  }      
};

//thermotron();
//plates();
//renderknob();
//renderservos();
//rendersteppers();
//rendercoupler();

projection() {
  difference() {
    platetiptop();
    platesubtract();  
  }    

}
translate([0, 150.5, 0]) projection() {
  difference() {
    platetop();
    platesubtract();    
  }
}
translate([150.5, 0, 0]) projection() {
difference() {    
 platemiddle();
 platesubtract();    
 }   
}
translate([150.5, 150.5, 0]) projection() {
difference() {    
 platebottom();
 platesubtract();    
 }    
}
