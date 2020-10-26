//long randNumber;

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
double randomDouble(double minf, double maxf)
{
  return minf + random(1UL << 31) * (maxf - minf) / (1UL << 31);  // use 1ULL<<63 for max double values)
}

void loop() {
  // print a random number from 0 to 100
//  randNumber = random(0,100);
//  Serial.print(randNumber);
  Serial.print(randomDouble(0.01, 4.00), 8);
  Serial.print('\n');

  // print a random number from 0 to -100
  //randNumber = -random(0,100);
  //Serial.print(randNumber);

  delay(50);
}
