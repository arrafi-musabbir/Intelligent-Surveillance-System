//----------------------------------------Load libraries
#include <esp_now.h>
#include <WiFi.h>
//----------------------------------------

uint8_t broadcastAddress[] = {0x94, 0xE6, 0x86, 0x05, 0xA4, 0xB8}; //--> REPLACE WITH THE MAC Address of your receiver / ESP32 Receiver.

//----------------------------------------Variables to accommodate the data to be sent.
int send_rnd_val_1;
int send_rnd_val_2;
//----------------------------------------

String success; //--> Variable to store if sending data was successful.

//----------------------------------------Structure example to send data
// Must match the receiver structure
typedef struct struct_message {
    int rnd_1;
//    int rnd_2;
} struct_message;

struct_message send_Data; //--> Create a struct_message to send data.
//----------------------------------------

#define BUZZER_PIN 12
const int trigPin = 26;
const int echoPin = 27;

//define sound speed in cm/uS
#define SOUND_SPEED 0.034

long duration;
float distanceCm;
float distanceInch;
int sensor_output;

const int PIR_SENSOR_OUTPUT_PIN = 13;  /* PIR sensor O/P pin */
int warm_up;

const int ledPin = 14;
// setting PWM properties
const int freq = 5000;
const int ledChannel = 0;
const int resolution = 8;

// Callback when data is sent
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
    Serial.print("\rLast Packet Send Status:\t");
    Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");

    if (status ==0){
        success = "Delivery Success :)";
      }
    else{
        success = "Delivery Fail :(";
      }
    Serial.println(">>>>>");
}


void setup() {
    Serial.begin(115200);
    pinMode(PIR_SENSOR_OUTPUT_PIN, INPUT);
    pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
    pinMode(echoPin, INPUT); // Sets the echoPin as an Input
    pinMode(BUZZER_PIN, OUTPUT);
    
    // configure LED PWM functionalitites
    ledcSetup(ledChannel, freq, resolution);
    // attach the channel to the GPIO to be controlled
    ledcAttachPin(ledPin, ledChannel);

    Serial.println("Waiting For Power On Warm Up");
    WiFi.mode(WIFI_STA); //--> Set device as a Wi-Fi Station.
    delay(1000);
    //Init ESP-NOW
    if (esp_now_init() != ESP_OK) {
        Serial.println("Error initializing ESP-NOW");
        return;
      }
    
    //  Once ESPNow is successfully Init, we will register for Send CB to
    //  get the status of Trasnmitted packet
    esp_now_register_send_cb(OnDataSent);
    //  Register peer
    esp_now_peer_info_t peerInfo;
    memcpy(peerInfo.peer_addr, broadcastAddress, 6);
    peerInfo.channel = 0;  
    peerInfo.encrypt = false;

    //  Add peer        
    if (esp_now_add_peer(&peerInfo) != ESP_OK){
        Serial.println("Failed to add peer");
        return;
      }
    delay(1000);
    Serial.println("Ready!");
}

void sonarDistance() {

    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPin, HIGH);
    
    // Calculate the distance
    distanceCm = duration * SOUND_SPEED/2;

    // Prints the distance in the Serial Monitor
     Serial.print("Distance covering (cm): ");
     Serial.println(distanceCm);

  }

void sendSignal() {
    //Send message via ESP-NOW
    send_Data.rnd_1 = 1;
    esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &send_Data, sizeof(send_Data));
    if (result == ESP_OK) {
       Serial.println("Sent with success");
      }
    else {
        Serial.println("Error sending the data");
      }
  }

void loop() {
  
  sonarDistance();
  ledcWrite(ledChannel, 50);
  if (distanceCm<40) {
      sensor_output = digitalRead(PIR_SENSOR_OUTPUT_PIN);
      if( sensor_output == LOW ) {
            Serial.println("Sonar triggered >>> scanning with PIR >>> No movement" );
            digitalWrite(BUZZER_PIN, LOW);
        }

      else {
          Serial.print("Motion detected at distance (cm):  ");
          Serial.println(distanceCm);
          digitalWrite(BUZZER_PIN, HIGH);
          Serial.println("capturing footage");
          Serial.println("sending intruder alert");
          sendSignal();
          delay(1000);
          digitalWrite(BUZZER_PIN, LOW);
          delay(1000);
        } 
  }

  delay(500);

}
