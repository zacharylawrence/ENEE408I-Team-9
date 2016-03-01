 
void setup() 
{ 
  Serial.begin(9600);
  while (!Serial);
} 

void loop() 
{ 
  if (Serial.available())
  {
    char data[9];
    // read 9 bytes
    Serial.readBytes(data, 9);
    if(data[0] != 1){
     // error 
     Serial.println("Header recieved was not 1");
    }
    
    int leftDirection = data[1]-0x30;
    int leftSpeed = data[2]-0x30;
    int rightDirection = data[5]-0x30;
    int rightSpeed = data[6]-0x30;    
    
  }
  
  // write sensor information
  sendPingData();
}

void sendPingData() {
  // read ping, send 9 bytes, header = 2
  
}

void setLeftMotorSpeed(float speed) {
  
}

void setRightMotorSpeed(float speed) {
  
}

