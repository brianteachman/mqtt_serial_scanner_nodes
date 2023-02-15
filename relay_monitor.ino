/*
 * Arduino Relay Serial Communication
 * 
 * Author:  Brian Teachman
 * Date:    02/03/2023
 */

//-----------------------------------------------------------

unsigned long previous_time = 0; // used for calculating run time

//-----------------------------------------------------------

const unsigned int relayPin = 16;
const unsigned int limitSwitch = 17;
const unsigned int ledPin = 25;

//-----------------------------------------------------------

void setup() {
  pinMode(relayPin, INPUT_PULLDOWN);
  pinMode(ledPin, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  
  // setup timer
  unsigned long this_time = millis();
  unsigned long running_time = this_time - previous_time;

  //--------------------------------------------------------

  String message = "";

  if ( digitalRead(relayPin) == HIGH ) {
    message = "Closed";
    digitalWrite(ledPin, HIGH);
  } else {
    message = "Opened";
    digitalWrite(ledPin, LOW);
  }
  Serial.println(message); // Send serial com to controller
  delay(10); // Small delay for stability

}
