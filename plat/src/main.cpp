#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <WebSocketsServer.h>
#include <Hash.h>

// Configuration
#define BUZZER_PIN 5
#define SERIAL_BAUD 115200
#define WEBSOCKET_PORT 80
#define WIFI_TIMEOUT 10  

// WiFi credentials
const char* WIFI_SSID = "ITAKADEMY-STUDENTS";
const char* WIFI_PASSWORD = "itakademy";

// Global objects
ESP8266WiFiMulti wifiMulti;
WebSocketsServer webSocket(WEBSOCKET_PORT);

void setupSerial();
void setupWiFi();
void setupWebSocket();
void handleWebSocketEvent(uint8_t num, WStype_t type, uint8_t* payload, size_t length);
void setBuzzerValue(const char* hexValue);
void printWiFiStatus();

void setup() {
    setupSerial();
    pinMode(BUZZER_PIN, OUTPUT);
    setupWiFi();
    setupWebSocket();
}

void loop() {
    webSocket.loop();
    
    // Print IP address every 30 seconds so we can change it on app.py
    static unsigned long lastPrint = 0;
    if (millis() - lastPrint > 30000) {
        printWiFiStatus();
        lastPrint = millis();
    }
}

void setupSerial() {
    Serial.begin(SERIAL_BAUD);
    Serial.println("\n\n=========================");
    Serial.println("SoundOff Buzzer Starting");
    Serial.println("=========================");
}

void printWiFiStatus() {
    Serial.println("\n------------------------");
    Serial.printf("Connected to: %s\n", WIFI_SSID);
    Serial.printf("Signal Strength: %d dBm\n", WiFi.RSSI());
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    Serial.printf("WebSocket Port: %d\n", WEBSOCKET_PORT);
    Serial.println("------------------------\n");
}

void setupWiFi() {
    WiFi.mode(WIFI_STA); 
    wifiMulti.addAP(WIFI_SSID, WIFI_PASSWORD);
    
    Serial.printf("\nConnecting to %s", WIFI_SSID);
 
    int timeout = 0;
    while (wifiMulti.run() != WL_CONNECTED && timeout < WIFI_TIMEOUT * 10) {
        delay(100);
        Serial.print(".");
        timeout++;
    }
    
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("\nWiFi connection FAILED");
        ESP.restart(); 
    }
    
    printWiFiStatus();
}

void setupWebSocket() {
    webSocket.begin();
    webSocket.onEvent(handleWebSocketEvent);
    Serial.printf("WebSocket server started on port %d\n", WEBSOCKET_PORT);
}

void handleWebSocketEvent(uint8_t num, WStype_t type, uint8_t* payload, size_t length) {
    switch (type) {
        case WStype_DISCONNECTED:
            Serial.printf("[%u] Client disconnected\n", num);
            break;
            
        case WStype_CONNECTED: {
            IPAddress ip = webSocket.remoteIP(num);
            Serial.printf("[%u] Client connected from %d.%d.%d.%d\n", 
                num, ip[0], ip[1], ip[2], ip[3]);
            webSocket.sendTXT(num, "Connected");
            break;
        }
            
        case WStype_TEXT:
            Serial.printf("[%u] Received: %s\n", num, payload);
            if (payload[0] == '#') {
                setBuzzerValue((const char*)&payload[1]);
            }
            break;
            
        default:
            break;
    }
}

void setBuzzerValue(const char* hexValue) {
    int value = (int)strtol(hexValue, NULL, 16);
    value = constrain(value, 0, 255); 
    
    Serial.printf("Setting buzzer to: %d\n", value);
    analogWrite(BUZZER_PIN, value);
}