long randNumber;

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // if analog input pin 0 is unconnected, random analog
  // noise will cause the call to randomSeed() to generate
  // different seed numbers each time the sketch runs.
  // randomSeed() will then shuffle the random function.
  randomSeed(analogRead(0));
}

void loop() {
  // print a random number from 0 to 100
  randNumber = random(0,100);
  Serial.print(randNumber);
  Serial.print('\n');

  // print a random number from 0 to -100
  //randNumber = -random(0,100);
  //Serial.print(randNumber);

  delay(50);
}
