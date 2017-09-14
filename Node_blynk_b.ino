/*************************************************************
  Download latest Blynk library here:
    https://github.com/blynkkk/blynk-library/releases/latest
  Blynk is a platform with iOS and Android apps to control
  Arduino, Raspberry Pi and the likes over the Internet.
  You can easily build graphic interfaces for all your
  projects by simply dragging and dropping widgets.
    Downloads, docs, tutorials: http://www.blynk.cc
    Sketch generator:           http://examples.blynk.cc
    Blynk community:            http://community.blynk.cc
    Social networks:            http://www.fb.com/blynkapp
                                http://twitter.com/blynk_app
  Blynk library is licensed under MIT license
  This example code is in public domain.
 *************************************************************
  This example runs directly on NodeMCU.
  Note: This requires ESP8266 support package:
    https://github.com/esp8266/Arduino
  Please be sure to select the right NodeMCU module
  in the Tools -> Board menu!
  For advanced settings please follow ESP examples :
   - ESP8266_Standalone_Manual_IP.ino
   - ESP8266_Standalone_SmartConfig.ino
   - ESP8266_Standalone_SSL.ino
  Change WiFi ssid, pass, and Blynk auth token to run :)
  Feel free to apply it to any other example. It's simple!
 *************************************************************/

/* Comment this out to disable prints and save space */
#define BLYNK_PRINT Serial


#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

// You should get Auth Token in the Blynk App.
// Go to the Project Settings (nut icon).
char auth[] = "5aaeedc15b99426cbd901b269754577b";
#define PINM V0
#define PIN_FEED D3
// Your WiFi credentials.
// Set password to "" for open networks.
char ssid[] = "network.lviv.ua";
char pass[] = "2016a2016";
char buffer[64];
void setup()
{
  // Debug console
  Serial.begin(9600);
  
  Blynk.begin(auth, ssid, pass);
  // You can also specify server:
  //Blynk.begin(auth, ssid, pass, "blynk-cloud.com", 8442);
  //Blynk.begin(auth, ssid, pass, IPAddress(192,168,1,100), 8442);
  pinMode(PINM, OUTPUT);
  pinMode(PIN_FEED,OUTPUT);
  pinMode(D2,OUTPUT);
}
int pinValue;
String rd;
int marker=0;

BLYNK_WRITE(V1)
{
  pinValue = param.asInt(); // assigning incoming value from pin V1 to a variable
  // You can also use:
  // String i = param.asStr();
  // double d = param.asDouble();
  
  
}

void loop()
{
  Blynk.run();
  //Serial.print("move-");
  //Serial.println(V1.asInt());
  
  if(digitalRead(D4)!=0){
    digitalWrite(PIN_FEED, HIGH);
  }else{
    digitalWrite(PIN_FEED, LOW); 
  }
  
  if(marker >= 300){
  while (Serial.available()==0) {
    
  }
  rd = Serial.readStringUntil(':');
  rd.toCharArray(buffer, sizeof(buffer) );
  Serial.println("------------------------");
  Serial.println(buffer);
  
  
  Blynk.virtualWrite(PINM,buffer);
  Serial.print("V1 Slider value is: ");
  Serial.print(pinValue);
  digitalWrite(D2,pinValue);
  Serial.println(pinValue);
  marker=0;
  }
  marker++;
}
