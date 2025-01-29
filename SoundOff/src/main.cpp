#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "ITAKADEMY-STUDENTS";
const char* password = "itakademy";
const int vibrationPin = 5; // D1 is GPIO5
ESP8266WebServer server(80);

void setup() {
    Serial.begin(115200);
    pinMode(vibrationPin, OUTPUT);
    digitalWrite(vibrationPin, LOW); // Ensure motor is off at startup

    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected!");

    server.on("/", HTTP_GET, []() {
        server.send(200, "text/html", "<html><body><h1>ESP8266 Vibration Control</h1><button onclick=\"fetch('/play')\">Play</button></body></html>");
    });

    server.on("/play", HTTP_GET, []() {
        Serial.println("START"); // Trigger Python script via Serial
        server.send(200, "text/plain", "Playing...");
    });

    server.begin();
    Serial.println("Web server started!");
}

void loop() {
    server.handleClient();
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        if (command == "START") {
            digitalWrite(vibrationPin, HIGH);
        } else if (command == "STOP") {
            digitalWrite(vibrationPin, LOW);
        }
    }
}
