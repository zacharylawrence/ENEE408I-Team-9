#define LEDPIN 13

void setup() {
  Serial.begin(9600);
  pinMode(LEDPIN, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    char key = Serial.read();
    
    if (key == 'h') {
      Serial.println("High");
      digitalWrite(LEDPIN, HIGH);
    } else if (key == 'l') {
      Serial.println("Low");
      digitalWrite(LEDPIN, LOW);
    }
  }
}
