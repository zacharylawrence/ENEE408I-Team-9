
int serial_found = 1;

void setup() {

  Serial.begin(9600); // Default connection rate for my BT module
}

void loop() {
  
  // If some data is sent, read it and save it in the state variable
  if(Serial.available() ){
    char state = Serial.read();
    Serial.println(state);
  } 
  else{
    serial_found = 0; 
  }

}
