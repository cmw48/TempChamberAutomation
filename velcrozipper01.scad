difference() {
cube([65,60,20]);
translate([20,0,0]) cube([25, 60, 5]);
    
}

translate([100,0,0])

difference() {
union() {    
translate([45,0,0])cube([25,60,10]);
translate([-25,0,0])cube([25,60,10]);
cube([45,60,40
    ]);   
    
}    
translate([20,0,0]) cube([5, 60, 25]);
    
}

translate ([25, 0, 0]) 
difference(){
union() {    
translate([45,100,0])cube([25,100,10]);
translate([-25,100,0])cube([25,100,10]);
translate([0,100,0]) cube([45,100,40
    ]);   
}
union() {
translate([20,150,0]) rotate(-20,0,0) cube([5, 60, 25]);
translate([20,150,0]) rotate(20,0,0) cube([5, 60, 25]);
translate([20,100,0]) rotate(0,0,0) cube([5, 60, 25]);
}
};