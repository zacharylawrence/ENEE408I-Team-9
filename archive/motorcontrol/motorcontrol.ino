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
    char key = Serial.read();
    if (key == 'f')
    {
      Serial.println("forward");
      setMotorDirection(MOTOR2, 0);
    }
    if (key == 'b')
    {
      Serial.println("backward");
      setMotorDirection(MOTOR2, 1);
    }
    if (key == 'u')
    {
      Serial.println("speedup");
      MOTOR2_speed += 50;
      setMotorSpeed(MOTOR2, MOTOR2_speed);
    }
    if (key == 'd')
    {
      Serial.println("speeddown");
      MOTOR2_speed -= 50;
      setMotorSpeed(MOTOR2, MOTOR2_speed);
    }
  }
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
