#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>
#include "time.h"
#include <esp_mac.h>

const char* ssid = "iPhone de Pedro";
const char* password = "sabotagem";

const char* mqtt_server = "test.mosquitto.org";
const int mqtt_port = 1883;
const char* mqtt_topic = "/roger/teste";

#define DHTPIN 13
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// char uid[64]; variavel timestamp-uid
char mac_address[13];

const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = -3 * 3600; // offset brasília 
const int   daylightOffset_sec = 0;

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  Serial.print("Conectando a ");
  Serial.println(ssid);
  delay(100);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("\nWiFi conectado!");
  Serial.println("IP: " + WiFi.localIP().toString());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Conectando ao MQTT...");
    if (client.connect("08D1F999F194")) {
      Serial.println("Conectado ao broker MQTT!");
      client.subscribe("/roger/teste");
    } else {
      Serial.print("Falhou, rc=");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  while (!Serial);
  dht.begin();
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);

  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);

  uint8_t mac[6];
  esp_read_mac(mac, ESP_MAC_WIFI_STA);

  struct tm timeinfo;
  while (!getLocalTime(&timeinfo)) {
    Serial.println("Aguardando sincronização do tempo...");
    delay(1000);
  }
  
  // snprintf(uid, sizeof(uid), "%lld-%02X%02X%02X%02X%02X%02X", Uid gerado com o Mac e Timestamp
  //          (long long)now, 
  //          mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);

  snprintf(mac_address, sizeof(mac_address), "%02X%02X%02X%02X%02X%02X",
          mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
           
  Serial.print("UID gerado: ");
  Serial.println(mac_address);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }

  client.loop();

  static unsigned long last_unixtime = 0;

  time_t now;
  time(&now);

  // if (now % 900 == 0 && now != last_unixtime ) {
  //   last_unixtime = now;

  // if (millis() - lastMsg > 2000) {
  //   lastMsg = millis();

  if (now % 20 == 0 && now != last_unixtime ) {
    last_unixtime = now;
    
    float temp = dht.readTemperature();
    float hum = dht.readHumidity();

    if (!isnan(temp) && !isnan(hum)) {
      StaticJsonDocument<100> doc;
      doc["temperatura"] = temp;
      doc["umidade"] = hum;
      doc["uid"] = mac_address;
      doc["unixtime"] = now;

      char payload[128];
      serializeJson(doc, payload);

      Serial.print("Enviando: ");
      Serial.println(payload);

      client.publish(mqtt_topic, payload);
    } else {
      Serial.println("Erro ao ler o DHT11");
    }
  }
}
