#include <Servo.h>

const int laserReceiverPin = 13;
Servo myservo;

// Stepper Motor
const int dirPin = 2;
const int stepPin = 3;
const int stepsPerRevolution = 50;  // 200 steps = 360 deg 

// Motor Driver PWM Pin
const int pwmPin = 5;  // PWM pin for motor control
const int motorSpeed = 100;  // Adjust speed (0-255)

void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(pwmPin, OUTPUT);

  myservo.attach(4);
  pinMode(laserReceiverPin, INPUT);
  
  Serial.begin(9600);
}

void loop() {
  int laserState = digitalRead(laserReceiverPin);

  if (laserState == HIGH) { 
    // Run motor at set speed
    analogWrite(pwmPin, motorSpeed);  
    // Serial.println("Motor Running - Laser HIGH");
    Serial.println(1);
  } 
  else {  
    // Serial.println("Detected - Executing Actions");

    // Stop Motor
    analogWrite(pwmPin, 0);
    delay(1000);  

    // Execute Stepper Function
    for(int x = 0; x < stepsPerRevolution; x++) {  
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(3500);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(3500);
    }

    // Capture webcam
    delay(1500);
    Serial.print(0);
    
    while(!Serial.available());
    int x = Serial.readString().toInt();
    Serial.print(x);
    if (x == 6) {
      myservo.write(45);
    } else {
      myservo.write(90);
    }

    // If defect, move stepper if not yet set to defect side?
    // If not defect, move stepper if not yet set to good side

     // Start Motor Again
    analogWrite(pwmPin, 120);
    delay(130);

    // Stop Motor
    analogWrite(pwmPin, 0);
  }
}