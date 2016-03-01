#include "pins.h"

void setup() {
  pinMode(13, OUTPUT);

  Serial.begin(9600);
  while (! Serial);
}


void loop() {
  if (Serial.available()) {
    // read 9 bytes
    unsigned char data[9];
    Serial.readBytes(data, 9);

    if (data[0] == 1 &&    // OpCode
        data[1] == 0 &&    // Left forward
        data[2] == 255 &&  // Left speed 255
        data[3] == 0 &&    // Right forward
        data[4] == 255 &&    // Right speed 255
        data[5] == 0) {  
      digitalWrite(13, HIGH);
    } else {
      digitalWrite(13, LOW);
    }

    Serial.println(data[2]);
  }
  
}
