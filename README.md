# ContinuousServoCharacterization
Characterizing the rotational speed of continuous rotation servos.

My son and I are getting into electronics and robotics.  I decided to start us off with a Raspberry Pi to control a servo.  Along the way I learned that there are a few kinds of servos with different characteristics.  I by chance had only purchased "continuous rotation servos", which means that I could control the direction of rotation and speed, but I did not have direct access to position.  I decided to start a project to allow me to characterize the different speed of rotation of the continuous rotation servo that I had ordered to see if I could get the best of both worlds (full rotation, speed control, position control).

##Servo Background
The servos I am dealing with use Pulse Width Modulation (PWM) for control.  There are two types of servos that I have become familiar with, one is limited range servos and continuous rotation servos.

###Limited Range Servos (aka Servo)
The width of the PWM signal drives the angle at which a limited range servo stops.  The most common servos have a total of 180 degree sweep, often +/- 90 degree from center.  The speed at which these servos move from position to position is fixed.  You give up control of the speed in order to have full control over position.

###Continuous Rotation Servo
The width of the PWM signal drives the rotation direction and speed of a continuous rotation servo.  Like the name implies the servo will continue spinning at the speed and direction as long as the appropriate signal is applied.  However, because of how continuous rotation servos are fabricated they do not provide an easy way to precisely control the position of the servo.  

###Continuous Rotation Servo with position feedback.
Adafruit now has a continuous rotation servo with an analog feedback signal that indicates the angle position of the servo.  I will play with these later, and I expect that this product will end up being my go-to for the scenario where I need full control over speed, direction, and position.


##Characterization
A future project my son and I want to do will require the knowledge of both servo control and computer vision.  I figured a good stepping stone would be to make a rig that could characterize the rotational speed of a continuous rotation servo.  The idea is that with the knowledge of the rotation speed, a starting point, and timing I should be able to somewhat precisely control the angle of a continous rotation servo.

A camera attached to the Raspberry Pi locates the servo starting point (a green dot on a servo arm).  The raspberry pi then drives the speed and direction of the servo until the arm returns to the starting point.  The time of that full rotation is captured.  This measurement is performed three times in order to find any variation for that speed and direction.  This is repeated for each of the distinct speeds that the servo can be driven.

The next step is to take this data, and come up with the timing the servo will need to run for that speed in order to move a specific angle.  I plan to come up with a library that will then allow the precise movement through an arc at a specific speed, all while tracking the postion of hte servo.  

##Hardware
###[FS5103R Continuous Rotation Server](https://www.adafruit.com/product/154)
My first servo purchase was the FS5103R from Aadfruit.  I had no knowledge of servos, and did not know what I was getting into. For the project I am working on I really needed to control the position of the servo, and not the speed/direction.  But since I was ignorant of the operation of servos I figured I would work with what I had ordered.


