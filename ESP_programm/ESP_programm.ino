#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

int LED_PINS[] = {16, 5, 4, 0};
int nb_leds = 4;


// PARTIE CONNEXION =====================================================================================================

// Update these with values suitable for your network.
const char* ssid = "Chiaomi";
const char* password = "akinoMD4C";

const char* mqtt_server = "192.168.123.26";
const int mqtt_port = 1883;

const char* mqtt_topic = "LEDS_PCO";
const String mqtt_clientid = "PCO_LEDS_ESP";

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
   delay(100);
  // We start by connecting to a WiFi network
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) 
    {
      delay(500);
      Serial.print(".");
    }
  randomSeed(micros());
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) 
  {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = mqtt_clientid;
    // Attempt to connect
    //if you MQTT broker has clientID,username and password
    //please change following line to    if (client.connect(clientId,userName,passWord))
    if (client.connect(clientId.c_str()))
    {
      Serial.println("connected");
     //once connected to MQTT broker, subscribe command if any
      client.subscribe(mqtt_topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 6 seconds before retrying
      delay(500);
    }
  }
} //end reconnect()



// PARTIE TRAITEMENT DES MESSAGES =====================================================================================================

// la fonction appelée à la réception d'un message MQTT
void callback(char* topic, byte* payload, unsigned int length) 
{
  String sMsg = "";

  for(int i = 0; i < length; i++) {
    //Serial.print((char)payload[i]);
    sMsg = sMsg + (char)payload[i];
  }

  // Parsing data as JSON of table row :
  const size_t capacity = JSON_OBJECT_SIZE(5);
  StaticJsonDocument<128> doc;

  auto error = deserializeJson(doc, sMsg);
  if (error) {
    Serial.print(F("deserializeJson() failed with code "));
    Serial.println(error.c_str());
    return;
  }

  // Decode JSON/Extract values
  int room_id = doc["room_id"];
  Serial.print("room_id :");
  Serial.println(room_id);
  
  if (room_id >= 0 && room_id < nb_leds)
  {
    
    bool variate = doc["variate"];
    Serial.print("variate :");
    Serial.println(variate);

    if (variate)
    {
      int lum_prct = doc["lum_prct"];
      Serial.print("luminosity :");
      Serial.println(lum_prct);

      float lum = lum_prct*255/100;
      analogWrite(LED_PINS[room_id], lum);
    }

    else
    {
      analogWrite(LED_PINS[room_id], 255);
    }
  }

}



// PARTIE SETUP ET LOOP =====================================================================================================

void setup() {
  Serial.begin(9600);
  for (int led_i = 0; led_i < nb_leds; led_i++) {
    pinMode(LED_PINS[led_i], OUTPUT);
    analogWrite(LED_PINS[led_i], LOW);
  }
  
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

// the loop function runs over and over again forever
void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

}
