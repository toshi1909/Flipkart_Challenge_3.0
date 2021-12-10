//communication 1 way
//firstly download library https://github.com/nRF24/RF24

#include <SPI.h>
//transmitter

#include <nRF24L01.h>
#include <RF24.h>
RF24 radio(9, 10); // CE, CSN         
const byte address[6] = "00001"; //Byte of array representing the address. This is the address where we will send the data. This should be same on the receiving side.
int button_pin = 2;
boolean button_state = 0;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
pinMode(button_pin, INPUT_PULLUP);
pinMode(button_pin, INPUT);
radio.begin();                  //Starting the Wireless communication
radio.openWritingPipe(address); //Setting the address where we will send the data
radio.setPALevel(RF24_PA_MIN);  //You can set it as minimum or maximum depending on the distance between the transmitter and receiver.
radio.stopListening();          //This sets the module as transmitter
}

String str="";
void loop()
{ char x[32];
  while (!Serial.available());
  str = Serial.readString();
  
  Serial.print(str);
  str.toCharArray(x,32);
  
  radio.write(x, sizeof(x));
  
  delay(10);
}
