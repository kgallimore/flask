/* Pump Controller Testing
* Author: Andrew Amerman
* 
* Arduino code that controls the pump through a variable voltage modifier.
* Relay alternates which direction the motor is going (change at 0rpm)
*
*/


const int pin_a = 3; // LOW
const int pin_b = 4; // Relay Enable (HIGH v. LOW for direction)
const int pin_c = 5; // LOW
const int pin_d = 6; // PWM
//const int pot_pin = A4;
boolean pump_direction = LOW;

void setup() {
  pinMode(pin_a, OUTPUT);
  pinMode(pin_b, OUTPUT);
  pinMode(pin_c, OUTPUT);
  pinMode(pin_d, OUTPUT);

  digitalWrite(pin_a, LOW);
  digitalWrite(pin_b, pump_direction);
  digitalWrite(pin_c, LOW);
}

//Note, 250 for analogWrite under load should be max, around 10.8V. any higher may be too fast
//Need to measure RPM to confirm this though. For quick ramp up/down testing, 0-255 is okay.

void loop() {
  for(int i=0; i<255; i++){
    if (i ==0){
      pump_direction = !pump_direction;
      digitalWrite(pin_b, pump_direction);
      delay(1000);
    }
    analogWrite(pin_d, i);
    delay(70);
  }
  for(int i=255; i>0; i--){
    analogWrite(pin_d, i);
    delay(70);
  }
}
