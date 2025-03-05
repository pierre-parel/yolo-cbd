#include <Servo.h>

Servo myservo;

// Stepper Motor
const int stepPin = 3;
const int stepsPerRevolution =25;  // 200 steps = 360 deg .

void setup() {`
  pinMode(stepPin, OUTPUT);

  myservo.attach(4);  
  Serial.begin(9600);
}

void loop() {

  for(int x = 0; x < stepsPerRevolution; x++) {  
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(3500);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(3500);
  }

  // Capture webcam
  delay(250);
  Serial.print(0);
  
  while(!Serial.available());
  int x = Serial.readString().toInt();
  Serial.print(x);
  if (x == 5) {
    myservo.write(45);
  } else {
    myservo.write(90);
  }
}