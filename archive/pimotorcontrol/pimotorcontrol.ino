#include "pins.h"

int MOTOR1_speed = 0;
int MOTOR2_speed = 0;
 
void setup() 
{ 
  pinMode(MOTOR1, OUTPUT);
  pinMode(MOTOR1_DIR_A, OUTPUT);
  pinMode(MOTOR1_DIR_B, OUTPUT);
  pinMode(MOTOR2, OUTPUT);
  pinMode(MOTOR2_DIR_A, OUTPUT);
  pinMode(MOTOR2_DIR_B, OUTPUT);
  
  setMotorDirection(MOTOR1, 0);
  setMotorDirection(MOTOR2, 0);
  Serial.begin(9600);
  while (! Serial);
} 
 
 
void loop() 
{ 
   if (Serial.available())
  {
    // read 9 bytes
    char data[9];
    Serial.readBytes(data, 9);
    if(data[0] != 1){
      // error 
      Serial.println("Header recieved was not 1");
    }    
    
    //setMotorSpeed(MOTOR2, 50);
    //setMotorDirection(MOTOR1, data[1]);
    //setMotorSpeed(MOTOR1, data[2]);
    //setMotorDirection(MOTOR2, data[3]);
    setMotorSpeed(MOTOR2, data[4]);
    
  }
  
  // write sensor information
  sendPingData();
} 

void sendPingData() {
  // read ping, send 9 bytes, header = 2
  
}

/*
*  Change motor direction
*  0-forward 1-backward
*/
void setMotorDirection(int motor, int dir){
   Serial.println("setmotordirection");
   if(motor == MOTOR1){
     digitalWrite(MOTOR1_DIR_A, !dir);
     digitalWrite(MOTOR1_DIR_B, dir);
   }
   else {
     digitalWrite(MOTOR2_DIR_A, !dir);
     digitalWrite(MOTOR2_DIR_B, dir);
   }
}

/*
* Change motor speed
* value between 0 and 255
*/
void setMotorSpeed(int motor, int speed){
    Serial.println("setmotorspeed");
    if(speed < 0) {
      analogWrite(motor, 0);
    }
    else if(speed > 255) {
      analogWrite(motor, 255);
    }    
    else {
      analogWrite(motor, speed);
    }
}
