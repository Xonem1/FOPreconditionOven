

int inByte = 0;         // incoming serial byte
String inData;
String PesoCode = "P\r\n";
float rand_peso = 0.0;

void setup() {
  // start serial port at 9600 bps:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  pinMode(2, INPUT);   // digital sensor is on digital pin 2
}

void loop() {
  // if we get a valid byte, read analog ins:
  if (Serial.available() > 0) {
    rand_peso = random(1, 1000) / 15.0;
    // get incoming byte:
    //char inByte = Serial.read();
    //inData += inByte;
    //Serial.print(inData);
    Serial.print("    ");
    Serial.print(rand_peso);
    Serial.println(" g    \r\n");
    //("    0.000 oz    \r\n");
    inData = "";
  }
}


