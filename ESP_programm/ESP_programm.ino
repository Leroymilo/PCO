#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

const int LED_PINS[] = {16, 5, 4, 0};
const int nb_leds = 4;

// Command variables

bool on_ = false;
bool detect[nb_leds];
bool variate[nb_leds];
int lum_prct[nb_leds];

// Control variables

int cur_room = 0;
bool motor_on = false;
bool is_on[nb_leds];

// PARTIE CONNEXION =====================================================================================================

// Update these with values suitable for your network.
const char* ssid = "";
const char* password = "";

const char* mqtt_server = "localhost";
const int mqtt_port = 1883;

const char* mqtt_topic_room = "room_command";
const char* mqtt_topic_global = "global_command";
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
      client.subscribe(mqtt_topic_room);
      client.subscribe(mqtt_topic_global);
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
  StaticJsonDocument<256> doc;

  auto error = deserializeJson(doc, sMsg);
  if (error) {
    Serial.print(F("deserializeJson() failed with code "));
    Serial.println(error.c_str());
    return;
  }

  if (topic == mqtt_topic_room)
  {
    int room_id = doc["room_id"];
    variate[room_id] = doc["variate"];
    detect[room_id] = doc["detect"];
    lum_prct[room_id] = doc["lum_prct"];
    
    update_room(room_id);
  }

  else if (topic == mqtt_topic_global)
  {
    on_ = doc["on_"];
    motor_on = on_;

    for (int i = 0; i < nb_leds; i++)
    {
      update_room(i);
    }
  }
}

void update_room(int room_id) {    
  if (room_id >= 0 && room_id < nb_leds)
  {
    if (!on_)
    {
      is_on[room_id] = false;
      return;
    }

    if (!detect[room_id] || (detect[room_id] && room_id == cur_room))
    {
      if (variate[room_id])
      {
        float lum = lum_prct[room_id]*255/100;
        analogWrite(LED_PINS[room_id], lum);
        is_on[room_id] = (lum > 0);
      }

      else
      {
        analogWrite(LED_PINS[room_id], 255);
        is_on[room_id] = true;
      }
    }

    else
    {
      analogWrite(LED_PINS[room_id], 0);
      is_on[room_id] = false;
    }
  }
}



// PARTIE RELEVE DATA =======================================================================================================

void push() {
  
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
  delay(10);
  push();

}
