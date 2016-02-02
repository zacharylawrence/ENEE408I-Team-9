const int motor1 = 3;
const int motor1_dir_A = 2;
const int motor1_dir_B = 4;
const int motor2 = 6; 
const int motor2_dir_A = 7;
const int motor2_dir_B = 8;

int motor1_speed = 0;
int motor2_speed = 0;
 
void setup() 
{ 
  pinMode(motor1, OUTPUT);
  pinMode(motor1_dir_A, OUTPUT);
  pinMode(motor1_dir_B, OUTPUT);
  pinMode(motor2, OUTPUT);
  pinMode(motor2_dir_A, OUTPUT);
  pinMode(motor2_dir_B, OUTPUT);
  
  setMotorDirection(motor1, 0);
  setMotorDirection(motor2, 0);
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
      setMotorDirection(motor1, 0);
    }
    if (key == 'b')
    {
      Serial.println("backward");
      setMotorDirection(motor1, 1);
    }
    if (key == 'u')
    {
      Serial.println("speedup");
      motor1_speed += 50;
      setMotorSpeed(motor1, motor1_speed);
    }
    if (key == 'd')
    {
      Serial.println("speeddown");
      motor1_speed -+ 50;
      setMotorSpeed(motor1, motor1_speed);
    }
  }
} 

/*
*  Change motor direction
*  0-forward 1-backward
*/
void setMotorDirection(int motor, int dir){
   Serial.println("setmotordirection");
   if(motor == motor1){
     digitalWrite(motor1_dir_A, !dir);
     digitalWrite(motor1_dir_B, dir);
   }
   else {
     digitalWrite(motor2_dir_A, !dir);
     digitalWrite(motor2_dir_B, dir);
   }
}

void setMotorSpeed(int motor, int speed){
    Serial.println("setmotorspeed");
    if (speed >= 0 && speed <= 255)
    {
      analogWrite(motor, speed);
    }    
}
