// Adafruit Motor shield library
// copyright Adafruit Industries LLC, 2009
// this code is public domain, enjoy!

#include <Arduino.h>
#include <AFMotor.h>

/*
#define DELAY 250
#define F_CPU 16000000
*/

// Some macros that make the code more readable
#define output_low(port,pin) port &= ~(1<<pin)
#define output_high(port,pin) port |= (1<<pin)
#define set_input(portdir,pin) portdir &= ~(1<<pin)
#define set_output(portdir,pin) portdir |= (1<<pin)
//Outputs are:
//LED0 = PB5
//LED1 = PB1
//LED2 = PB2
//LED3 = PD3
//LED4 = PD5
//LED5 = PD6

/*
void delay_ms (unsigned int ms) {
  unsigned int16_t delay_count = F_CPU / 17500;
  volatile unsigned int16_t i;
  while (ms != 0) {
    for (i = 0; i != delay_count; i++);
    ms--;
  }
} // delay_ms

void delay() {
  long d;
  unsigned char oldb,oldd;
  for (d=0; d<DELAY; d++) {
    delay_ms(1);
    if ((PINC & 0b00001000)==0) {
      oldb = PORTB;
      oldd = PORTD;
      PORTB = 0xFF;
      PORTD = 0xFF;
      delay_ms(1);
      PORTB = oldb;
      PORTD = oldd;
      d--;
    } else {
      if ((PINC & 0b00000100)==0)
        d--;
      else
        delay_ms(1);
    } // if button pressed
  } // if button pressed
} // delay
*/


AF_DCMotor motorL(1, MOTOR12_64KHZ);
AF_DCMotor motorR(2, MOTOR12_64KHZ);

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }
  Serial.println("READY!");

  // turn on motor
  motorR.setSpeed(150);
  motorL.setSpeed(150);
 
  motorR.run(RELEASE);
  motorL.run(RELEASE);
}

void backward(unsigned int i) {
  motorR.run(FORWARD);
  motorL.run(FORWARD);
  delay(i);
}

void forward(unsigned int i) {
  motorR.run(BACKWARD);
  motorL.run(BACKWARD);
  delay(i);
}

void turn_left(unsigned int i) {
  motorR.run(BACKWARD);
  motorL.run(FORWARD);
  delay(i);
}

void turn_right(unsigned int i) {
  motorR.run(FORWARD);
  motorL.run(BACKWARD);
  delay(i);
}

void stop() {
  motorR.run(RELEASE);
  motorL.run(RELEASE);
}

void speed(unsigned int s) {
  motorR.setSpeed(s);
  motorL.setSpeed(s);
}

void loop() {
  int c;
  if (Serial.available() > 0) {
    c = Serial.read();
    Serial.write(c);
    if (c == 'w') {
      forward(500);
    } else if (c == 's') {
      backward(500);
    } else if (c == 'a') {
      turn_left(150);
    } else if (c == 'd') {
      turn_right(150);
    } else if (c == 'W') {
      forward(1000);
    } else if (c == 'S') {
      backward(1000);
    } else if (c == 'A') {
      turn_left(1000);
    } else if (c == 'D') {
      turn_right(1000);
    } else if (c == '0') {
      speed(150);
    } else if (c == '9') {
      speed(255);
    }
    stop();
  }
}
