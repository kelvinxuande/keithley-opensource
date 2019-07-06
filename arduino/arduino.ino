// Arduino input support for keithley_openSource
// Reference and setup visualisation:
// Basic state change detection: https://www.arduino.cc/en/Tutorial/StateChangeDetection

const int  buttonPin = 2;    // pin for pushButton
const int ledPin = 13;       // pin for feedback LED

int buttonState = 0;         // current state of the button
int lastButtonState = 0;     // previous state of the button

void setup() {
  // initialize the button pin as a input:
  pinMode(buttonPin, INPUT);
  // initialize the LED as an output:
  pinMode(ledPin, OUTPUT);
  // initialize serial communication:
  Serial.begin(9600);       // open serial monitor at baud rate for visual and/ or debugging
}

void loop() {
  // read pushbutton input pin:
  buttonState = digitalRead(buttonPin);
  // compare the buttonState to its previous state
  if (buttonState != lastButtonState) {
    if (buttonState == HIGH) {
      // if the current state is HIGH and the button went from off to on:
      Serial.println("Button Pressed");
    }
    // Delay to avoid switch bouncing
    delay(50);
  }
  // save the current state as the last state, for next time through the loop
  lastButtonState = buttonState;
}
