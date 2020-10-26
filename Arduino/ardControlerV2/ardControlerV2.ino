// Based on code written by Nikhil Uplekar, Nathan Koenigsmark, Huy Do
// ENEE408I Fall 2019 Team 2 December 2019
// revised 2020-10-17

// Code for robot Arduino, takes serial inputs, runs RTOS to multitask
// RTOS Background and examples. Be sure to add the FreeRTOS library to your Arduino code:
// https://circuitdigest.com/microcontroller-projects/arduino-freertos-tutorial1-creating-freertos-task-to-blink-led-in-arduino-uno

// Order API between robot computer and Arduino (no whitespace. Just the newlines)
//  forward -> f
//  left -> l
//  right -> r
//  backwards -> b
//  halt -> h
//  autoOn -> o
//  autoOff -> z
//  personFollow -> p
//  aprilFollow -> a

//#include <Arduino_FreeRTOS.h>
#include <FreeRTOS.h>
#include "MotorControl.h"
#include "Ultrasound.h"

//#define portCHAR char // Not used: See https://forum.arduino.cc/index.php?topic=667888.0

//constants
byte PWM = 60; // Effectively motor speed setting
const int STOP_DISTANCE_CENTER = 15; // cm Stopping distance for the center Ping sensor
const int STOP_DISTANCE_SIDE   = 10; // cm Stopping distance for the two side Ping sensors

// enum for Directions of robot movement. Modify for more directions, such as slight right turn, etc. 
enum Directions {forward, backward, left, right, halt};
  // 0 - forward, 1 - backwards, 2 - left, 3 - right, 4 - halt
  
// enum for type of following or avoidance of a person or an April tag
enum Following {person, april};
  // 0 - person, 1 - april

//globals for motor control
boolean avoidObstaclesEnabled = false; // Default to false
boolean freeRoam = false; // Not supported at this point, but useful in the future for patrolling
Directions currDir = halt;
Directions prevDir = halt;
Following followType = person; // Default to person following

//globals for obstacle avoidance, referring to the Ping sensors
boolean dangerCenter = false;
boolean dangerLeft   = false;
boolean dangerRight  = false;
boolean dangerDetected = false;
long leftDistance = 0, centerDistance = 0, rightDistance = 0;
boolean lastCommandFromSerial = false;

// Prototypes for RTOS tasks. See the tutorial:
// https://circuitdigest.com/microcontroller-projects/arduino-freertos-tutorial1-creating-freertos-task-to-blink-led-in-arduino-uno
void updateOrders  (void *pvParameters);
void updatePingData(void *pvParameters);
void driveACR      (void *pvParameters);

// Ping sensor signaling pin connections, modify as needed
// This assumes 3-pin Ping sensors from Parallax. 
const int center_ping_pin = 4;
const int left_ping_pin   = 7;
const int right_ping_pin  = 8;

/*
// Modify if have the low cost HC-SR04 that has 4 pins, see: https://gist.github.com/flakas/3294829
// VCC connection of the sensor attached to +5V
// GND connection of the sensor attached to ground
const int TRIG = 2 // HC-SR-0 TRIG pin to digital pin 2 or as you desire
const int ECHO = 4 // HC-SR-0 ECHO pin to digital pin 4 or as you desire
*/

// Motor pin connections, modify to match your setup
const int LeftMotorA_pin    = 11;
const int RightMotorA_pin   = 13;
const int LeftMotorB_pin    = 10;
const int RightMotorB_pin   = 12;
const int LeftMotorPWM_pin  = 6;
const int RightMotorPWM_pin = 5;

// Initializations of the motor and sensor objects, see MotorControl.h, Ultrasound.h
// Modify here and above if you have more or less sensors or motors
MotorControl leftMotor  (LeftMotorA_pin,  LeftMotorB_pin,  LeftMotorPWM_pin);
MotorControl rightMotor (RightMotorA_pin, RightMotorB_pin, RightMotorPWM_pin);
Ultrasound leftUltrasound   (left_ping_pin);
Ultrasound centerUltrasound (center_ping_pin);
Ultrasound rightUltrasound  (right_ping_pin);

void setup() {
  Serial.begin(9600); // Set baud-rate
  // Create RTOS tasks and set their priorities
  xTaskCreate(driveACR,       (const char *) "Driving",         128, NULL, 1, NULL); // Priority 1
  xTaskCreate(updateOrders,   (const char *) "Updating Orders", 128, NULL, 2, NULL); // Priority 2
  xTaskCreate(updatePingData, (const char *) "Updating Pings",  128, NULL, 3, NULL); // Priority 3
 /********************
//  xTaskCreate(driveACR,       (const portCHAR *) "Driving",         128, NULL, 1, NULL); // Priority 1
//  xTaskCreate(updateOrders,   (const portCHAR *) "Updating Orders", 128, NULL, 2, NULL); // Priority 2
//  xTaskCreate(updatePingData, (const portCHAR *) "Updating Pings",  128, NULL, 3, NULL); // Priority 3
*********************/
  go_stop(); // Guarantee that both motors are not moving at start
  set_speed(PWM, PWM); // Kind-of useless since we set it on every movement command (see below)
}

// This is empty, which lets RTOS run uninterupted and control events
void loop() {
}

void set_speed(const int left_speed, const int right_speed) {
  leftMotor.setPWM(left_speed);
  rightMotor.setPWM(right_speed); 
}

void go_stop() {
  leftMotor.halt();
  rightMotor.halt();
}

void go_forward() {
  // Motor speeds are set the same by default
  // You may have to adjust this if your motors
  // are not matched
  const int forwardSpeedOffset = 0
  set_speed(PWM + forwardSpeedOffset, PWM);
  leftMotor.forward();
  rightMotor.backward();
}

void go_backward() {
  // Motor speeds are set the same by default
  // You may have to adjust this if your motors
  // are not matched
  const int backwardSpeedOffset = 0 
  set_speed(PWM + backwardSpeedOffset, PWM);
  leftMotor.backward();
  rightMotor.forward();
}

void go_left() {
  set_speed(PWM, PWM);
  leftMotor.backward();
  rightMotor.backward();
}

void go_right() {
  set_speed(PWM, PWM);
  leftMotor.forward();
  rightMotor.forward();
}

void respondToCurrDir() {
  // TODO - if lastCommand was not from serial data, then don't check the currDir != prevDir
  
  // Only need to act on the currDir value if it's different from the prevDir
  if (currDir != prevDir) {
    if (currDir == forward)
      go_forward();
    else if (currDir == left)
      go_left();
    else if (currDir == right)
      go_right();
    else if (currDir == backward)
      go_backward();
    else if (currDir == halt)
      go_stop();
    else
      Serial.println("Error in respondToCurrDir() - currDir not found");
  }
}

//check the orders string for new commands
void updateOrders(void *pvParameters){ 
  while(1) {
    if(Serial.available() > 0) {
      char incomingCharacter = Serial.read();
      switch(incomingCharacter) {
        case '\n': // Disregard newlines
          break;
        case 'f':
          prevDir = currDir; 
          currDir = forward;
          lastCommandFromSerial = true;     
          break;
        case 'l':
          prevDir = currDir; 
          currDir = left;
          lastCommandFromSerial = true;      
          break;
        case 'r':
          prevDir = currDir;  
          currDir = right;
          lastCommandFromSerial = true;         
          break;
        case 'b': 
          prevDir = currDir; 
          currDir = backward;
          lastCommandFromSerial = true;     
          break;
        case 'h': 
          prevDir = currDir; 
          currDir = halt;
          lastCommandFromSerial = true;          
          break;
        case 'o': 
          avoidObstaclesEnabled = true;  
          break;
        case 'z': 
          avoidObstaclesEnabled = false; 
          break;
        case 'p':
          followType = person;
          break;
        case 'a':
          followType = april;
          break;
        default: 
          Serial.println("ERROR: Bad Message from Serial - character was not expected"); 
          break;
      }
    }
    vTaskDelay(50/ portTICK_PERIOD_MS);
  }
}

//check sensors for new obstacles
void updatePingData(void *pvParameters) {
  while(1) {
    // Get distances
    leftDistance   = leftUltrasound.getDistance();
    centerDistance = centerUltrasound.getDistance();
    rightDistance  = rightUltrasound.getDistance();
    
    // Update danger booleans
    dangerLeft   = leftDistance   <= STOP_DISTANCE_SIDE;
    dangerCenter = centerDistance <= STOP_DISTANCE_CENTER;
    dangerRight  = rightDistance  <= STOP_DISTANCE_SIDE;
    dangerDetected = dangerCenter || dangerRight || dangerLeft;
    
    vTaskDelay(150 / portTICK_PERIOD_MS);
  }
}

//drives the robot accoring to the last received order
void driveACR(void *pvParameters) {
  while(1) {
    
    // Print logs below... uncomment what's needed
    // ---------------------------------------------
    //Serial.print("L: "); Serial.print(leftDistance);Serial.print("      C: "); Serial.print(centerDistance);Serial.print("      R: "); Serial.println(rightDistance);
    //Serial.print("Current Direction : "); Serial.println(currDir);
    //Serial.print("Avoid enabled : "); Serial.println(avoidObstaclesEnabled);

    // Planning breakdown
    // ---------------------------------------------
    // We should have a 'FREE ROAM' boolean that, if enabled, does what the below currently does (moves all around stuff)
    // If we aren't free roaming - then we can assume that we're following something - in that case we can have 2 choices (based on avoidObstaclesEnabled)
    // If not avoiding.. then do not allow forward movement and only allow left turns and right turns
    // If avoiding is on, then we should come up with a way to get around obstacles ... hard to do
    // why? Because our vision code is continually sending stuff in response to our movments - 
    // we'll have to shut it up for a while and get around an obstacles and then re-enable it... hard to do

    if (!avoidObstaclesEnabled) { // avoidObstaclesEnabled is False, so just listen to commands from serial and act accordingly
      respondToCurrDir();
    }
    else { // avoidObstaclesEnabled is True 
      
      // Two variations of obstacle avoidance...
      //  1) Person following - just halt on obstacles
      //  2) April Tag following - actual obstacle avoidance

      // We should activley avoid obstacles (as long as we are not currently halted)...
      if (dangerDetected) { // If danger detected
        // SAVE FOR LATER: (dangerDetected && (currDir != halt)// If danger detected AND we're not currently in halt mode...
        
        if (followType == person) {
          // Person following responds to serial commands, but ignores them and halts when we're in danger.
          // EXCEPT left, right, and halt commands (which we should let through)...

          if (currDir == left || currDir == right || currDir == halt) {
            // Current direction is left/right/halt, so lets let the robot move that way
            respondToCurrDir();
          }
          else {
            lastCommandFromSerial = false;
            go_stop();
          }        
        }
        else if (followType == april) {
          // April following needs to do full avoidance
          // When avoiding something, we need to remove control from the serial commands and then restore them
          // TODO - for now lets just respond to current serial commands
          respondToCurrDir();

          // Check where the danger is...
          /*       
          if (centerDistance <= STOP_DISTANCE_CENTER) { // Danger at center...
            // Check whether we should go left or right
            if (leftDistance <= rightDistance) { // Right has more room than left, so go right.
                lastCommandFromSerial = false;  
                go_right();
            }
            else { // Left has more room than right, so go left.
                lastCommandFromSerial = false;    
                go_left();
            }
          }
          else if (leftDistance <= STOP_DISTANCE_SIDE) { // Issue @ left, so go right
              lastCommandFromSerial = false;  
              go_right();
          }
          else if (rightDistance <= STOP_DISTANCE_SIDE) { // Issue @ right, so go left
              lastCommandFromSerial = false;  
              go_left();
          }
          else { // No issue - this shouldn't be possible
              Serial.println("error: this shouldn't be possible"); 
          }*/
        }
        else { // Neither followType matched... not possible
          Serial.println("ERROR: followType had no match"); 
        }
      }
      else { // Else no danger detected...
        // In this scenario, we should just respond to the command we've been given by calling respondToCurrDir().
        // BUT, if we are in the process of avoiding an obstacle, then we need to have the forward-motion
        // to get out of the area first. If that last command was not from serial
        respondToCurrDir();
      }
    }
    
    vTaskDelay(50 / portTICK_PERIOD_MS);
  }
}

// The code below is old code used to have the robot free roam around the room while avoiding anything
// that falls into its path

//        // Check where the danger is...
//        
//        if (centerDistance <= STOP_DISTANCE_CENTER) { // If Danger at center...
//          // Check whether we should go left or right
//          if (leftDistance <= rightDistance) { // Right has more room than left, so go right.
//              lastCommandFromSerial = false;  
//              prevDir = currDir;
//              currDir = right;
//              respondToCurrDir();
//          }
//          else { // Left has more room than right, so go left.
//              lastCommandFromSerial = false;  
//              prevDir = currDir;
//              currDir = left;
//              respondToCurrDir();
//          }
//        }
//        else if (leftDistance <= STOP_DISTANCE_SIDE) { // Issue @ left, so go right
//            lastCommandFromSerial = false;  
//            prevDir = currDir;
//            currDir = right;
//            respondToCurrDir();
//        }
//        else if (rightDistance <= STOP_DISTANCE_SIDE) { // Issue @ right, so go left
//            lastCommandFromSerial = false;  
//            prevDir = currDir;
//            currDir = left;
//            respondToCurrDir();
//        }
//        else { // No issue - this shouldn't be possible
//            Serial.println("error: this shouldn't be possible"); 
//        }
