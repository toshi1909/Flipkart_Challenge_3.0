//communication 1 way
//firstly download library https://github.com/nRF24/RF24

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(8, 48); // CE, CSN
const byte address[6] = "00001";
int led_pin = 3;
boolean button_state = 0;
int mh11 = 30;
int mh12 = 28;
int mh21= 26;
int mh22= 24;
int mh1e= 4;
int mh2e= 5;

int mv11 = 44;
int mv12 = 42;
int mv21= 38;
int mv22= 40;
int mv1e= 6;
int mv2e= 7;

int servo=3;

int pwm1;
int pwm2;

void setup() {
  
  pinMode(mh11, OUTPUT);
  pinMode(mh12, OUTPUT);
  pinMode(mh21, OUTPUT);
  pinMode(mh22, OUTPUT);
  pinMode(mh1e, OUTPUT);
  pinMode(mh2e, OUTPUT);


  pinMode(mv11, OUTPUT);
  pinMode(mv12, OUTPUT);
  pinMode(mv21, OUTPUT);
  pinMode(mv22, OUTPUT);
  pinMode(mv1e, OUTPUT);
  pinMode(mv2e, OUTPUT);
  
  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(0, address);   //Setting the address at which we will receive the data
  radio.setPALevel(RF24_PA_MIN);       //You can set this as minimum or maximum depending on the distance between the transmitter and receiver.
  radio.startListening();              //This sets the module as receiver
}



void loop()
{
  if (radio.available())              //Looking for the data.
  {
    char text[32] = "";                 //Saving the incoming data
    radio.read(&text, sizeof(text));    //Reading the data
    //radio.read(&button_state, sizeof(button_state));    //Reading the data

    pwm1=text[2]*10+text[3];
    pwm1 = (pwm1*255)/100;
    
    pwm2=text[4]*10+text[5];
    pwm2 = (pwm2*255)/100;

    Serial.print(pwm1,DEC);
    Serial.print(pwm2,DEC);
    if(text[0]=='1'){
      if(text[1] == 'D')
      {
        Serial.println(text);
        digitalWrite(mv11, HIGH);
        digitalWrite(mv12, LOW);
        digitalWrite(mv21, HIGH);
        digitalWrite(mv22, LOW);

        digitalWrite(mh11, LOW);
        digitalWrite(mh12, LOW);
        digitalWrite(mh21, LOW);
        digitalWrite(mh22, LOW);
        
        analogWrite(mv1e,pwm1);
        analogWrite(mv2e,pwm2);
      }
      else if(text[1] == 'U')
      {
        Serial.println(text);
        digitalWrite(mv11, LOW);
        digitalWrite(mv12, HIGH);
        digitalWrite(mv21, LOW);
        digitalWrite(mv22, HIGH);

        digitalWrite(mh11, LOW);
        digitalWrite(mh12, LOW);
        digitalWrite(mh21, LOW);
        digitalWrite(mh22, LOW);
        
        analogWrite(mv1e,pwm1);
        analogWrite(mv2e,pwm2);
      }
      else if(text[1] == 'L')
      {
        Serial.println(text);
        digitalWrite(mh11, HIGH);
        digitalWrite(mh12, LOW);
        digitalWrite(mh21, HIGH);
        digitalWrite(mh22, LOW);

        digitalWrite(mv11, LOW);
        digitalWrite(mv12, LOW);
        digitalWrite(mv21, LOW);
        digitalWrite(mv22, LOW);
        
        analogWrite(mh1e,pwm1);
        analogWrite(mh2e,pwm2);
      }
      else if(text[1] == 'R')
      {
        Serial.println(text);
        digitalWrite(mh11, LOW);
        digitalWrite(mh12, HIGH);
        digitalWrite(mh21, LOW);
        digitalWrite(mh22, HIGH);

        digitalWrite(mv11, LOW);
        digitalWrite(mv12, LOW);
        digitalWrite(mv21, LOW);
        digitalWrite(mv22, LOW);
        
        analogWrite(mh1e,pwm1);
        analogWrite(mh2e,pwm2);
      }
      else if(text[1] == 'T')
      {
        Serial.println("Serveo");
      }
    }
    
       // Serial.println(text);
  }
  delay(5);
}
