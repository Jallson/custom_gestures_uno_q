// NEW PROJECT: HAND GESTURES controlled ROBOTIC ARM

#include "Arduino_RouterBridge.h"
#include "Servo.h"
#include <Arduino_LED_Matrix.h>

// ============================================================
// LED MATRIX
// ============================================================

Arduino_LED_Matrix matrix;

const uint32_t smiley_face[] = {
  0x000200a8,
  0x0a802000,
  0x04403e00,
  0x00000000
};

// ============================================================
// SERVOS
// ============================================================

Servo servoPan;
Servo servoTilt;
Servo servoClaw;

// ============================================================
// PINS
// ============================================================

const int panPin = 9;
const int tiltPin = 10;
const int clawPin = 11;

// ============================================================
// POSITIONS
// ============================================================

int panPos = 90;
int tiltPos = 120;
int clawPos = 40;

// ============================================================
// SETUP
// ============================================================

void setup() {

  Serial.begin(115200);

  matrix.begin();

  servoPan.attach(panPin);
  servoTilt.attach(tiltPin);
  servoClaw.attach(clawPin);

  servoPan.write(panPos);
  servoTilt.write(tiltPos);
  servoClaw.write(clawPos);

  // ==========================================================
  // BRIDGE START
  // ==========================================================

  if (!Bridge.begin()) {
    Serial.println("Cannot setup Bridge");
  }

  if (!Monitor.begin()) {
    Serial.println("Cannot setup Monitor");
  }

  // ==========================================================
  // PROVIDE FUNCTION
  // ==========================================================

  Bridge.provide("set_arm", set_arm);

  Serial.println("Robotic Arm Ready");
}

// ============================================================
// LOOP
// ============================================================

void loop() {

}

// ============================================================
// FUNCTION CALLED FROM PYTHON
// ============================================================

void set_arm(int pan, int tilt, int claw) {

  panPos = constrain(pan, 10, 170);
  tiltPos = constrain(tilt, 60, 160);
  clawPos = constrain(claw, 40, 100);

  servoPan.write(panPos);
  servoTilt.write(tiltPos);
  servoClaw.write(clawPos);

  matrix.loadFrame(smiley_face);

  Monitor.print("PAN: ");
  Monitor.print(panPos);

  Monitor.print(" TILT: ");
  Monitor.print(tiltPos);

  Monitor.print(" CLAW: ");
  Monitor.println(clawPos);
}