// ---------------------------------------------------------------------------
// Measure distance from sensor to surface, calculate volume and total filling (percentage).
// Results in open serial monitor at 115200 baud to see ping results.
// ---------------------------------------------------------------------------

#include <NewPing.h>
#include <math.h> 

#define TRIGGER_PIN  12  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     11  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

float L = 100; //Lenght of tank
float R = 100; //Radius of tank
float H = 0; //Sensors height above cylinder
float D = 0; //Depth of shit
float D2 = 0; //Distance from sensor 
float V = 0; //Volume of shit
float VFULL = 0;
float VL = 0; //Volume in litres
float VP = 0; //Volume of shit in percent
const float pi = 3.1415;

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

void setup() {
  Serial.begin(115200); // Open serial monitor at 115200 baud to see ping results.
}

void loop() {
  delay(1000);                      // Wait 1s between pings. 29ms should be the shortest delay between pings.
  unsigned int uS = sonar.ping(); // Send ping, get ping time in microseconds (uS).
  D2=uS / US_ROUNDTRIP_CM; // Convert ping time to distance and print result (0 = outside set distance range, no ping echo)

  Serial.print("Distance to the surface from sensor: ");
  Serial.print(D2,0);
  Serial.println(" cm");
  
  Serial.print("How deep is you shit: ");
  D=2*R+H-D2;
  Serial.print(D,0); // Depth of shit
  Serial.println(" cm");
  
  V = ((L*sq(R)*acos((R-D)/R))-(R-D)*sqrt(2*R*D-sq(D)));
  VFULL = pi*sq(R)*L;
  VP = (V/VFULL*100);
  VL = V/1000;

  Serial.print("Volume of shit at the moment: ");
  Serial.print(V,0);
  Serial.println(" cm3");
  Serial.print("Percent full: ");
  Serial.print(VP,0);
  Serial.println("%");
  Serial.print("Max volume ");
  Serial.print(VFULL,0);
  Serial.println(" cm3");
  Serial.print("Litres of shit: ");
  Serial.print(VL,0);
  Serial.println("l");
  Serial.println("");

  
 
}
