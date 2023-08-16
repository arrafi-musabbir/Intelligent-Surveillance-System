//----------------------------------------Load libraries
#include <esp_now.h>
#include <WiFi.h>

#define BUZZER_PIN 12

//CC:DB:A7:64:73:D4
uint8_t broadcastAddress[] = {0xCC, 0xDB, 0xA7, 0x64, 0x73, 0xD4};


//----------------------------------------
char cmd;
//----------------------------------------Define variables to store incoming readings
int receive_rnd_val_1;
//----------------------------------------

//----------------------------------------Structure example to receive data
// Must match the sender structure
typedef struct struct_message {
    int rnd_1;
//    int rnd_2;
} struct_message;

struct_message receive_Data; //--> Create a struct_message to receive data.
struct_message send_data;

esp_now_peer_info_t peerInfo;

//----------------------------------------
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ VOID SETUP
void setup() {
  Serial.begin(115200);
  
  pinMode(BUZZER_PIN, OUTPUT);
//  uniformed();
//
//animal();
//
//nonuniformed();
//alert();
  WiFi.mode(WIFI_STA); //--> Set device as a Wi-Fi Station

  //----------------------------------------Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Once ESPNow is successfully Init, we will register for Send CB to
  // get the status of Trasnmitted packet
  esp_now_register_send_cb(OnDataSent);
  
  // Register peer
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  
  // Add peer        
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }
  //----------------------------------------
  
  esp_now_register_recv_cb(OnDataRecv); //--> Register for a callback function that will be called when data is received
}
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


// Callback when data is sent
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
//  Serial.print("\r\nLast Packet Send Status:\t");
//  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
//  if (status ==0){
//    success = "Delivery Success :)";
//  }
//  else{
//    success = "Delivery Fail :(";
//  }
}



//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ Callback when data is received
void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  memcpy(&receive_Data, incomingData, sizeof(receive_Data));
//  Serial.println();
//  Serial.println("<<<<< Receive Data:");
//  Serial.print("Bytes received: ");
//  Serial.println(len);
  receive_rnd_val_1 = receive_Data.rnd_1;
//  receive_rnd_val_2 = receive_Data.rnd_2;
//  Serial.println("Receive Data: ");
//  Serial.println(receive_rnd_val_1);
//  Serial.println(receive_rnd_val_2);
//  Serial.println("<<<<<");
  
  if (receive_rnd_val_1==1){
    alert();
    Serial.print("Recording feed from Camera \n");


}
  
  if (receive_rnd_val_1==2){
    nonuniformed();
    Serial.print("Recording feed from Camera \n");


}
  
  if (receive_rnd_val_1==3){
    animal();
    Serial.print("Recording feed from Camera \n");


}
  
  if (receive_rnd_val_1==4){
    uniformed();
    Serial.print("Recording feed from Camera \n");


}

  }
  
void nonuniformed(){
  for(int i=0;i<3;i++){
    Serial.println("non-uniformed person");
    digitalWrite(BUZZER_PIN, HIGH);
    delay(500);
    digitalWrite(BUZZER_PIN, LOW);
    delay(500);
//    delay(500);
  }
}

void uniformed(){
  for(int i=0;i<5;i++){
    Serial.println("uniformed person");
    digitalWrite(BUZZER_PIN, HIGH);
    delay(1000);
    digitalWrite(BUZZER_PIN, LOW);
    delay(1000);
//    delay(500);
  }
//  digitalWrite(BUZZER_PIN, HIGH);
}

void animal(){
    Serial.println("animal");
    digitalWrite(BUZZER_PIN, HIGH);
    delay(2000);
    digitalWrite(BUZZER_PIN, LOW);
    delay(1000);
//  digitalWrite(BUZZER_PIN, HIGH);
}


void alert(){
    Serial.println("normal alert");
    digitalWrite(BUZZER_PIN, HIGH);
    delay(1000);
    digitalWrite(BUZZER_PIN, LOW);
    delay(1000);
//  digitalWrite(BUZZER_PIN, HIGH);
}

void loop() {
   if (Serial.available())
    { 
    esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &send_data, sizeof(send_data));
    cmd=(Serial.read());
    Serial.println(cmd);
    if (cmd=='a'){
      uniformed();
    }
    else if (cmd=='s'){
      nonuniformed();
    }
    else if (cmd=='d'){
      animal();
    }
    else if (cmd=='f'){
      alert();
    }
     
  if (result == ESP_OK) {
      Serial.println("Sent with success");
    }
    else {
      Serial.println("Error sending the data");
    }
}
}
