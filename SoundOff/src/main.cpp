#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

const char* ssid = "ITAKADEMY-STUDENTS";
const char* password = "itakademy";

ESP8266WebServer server(80);

// Function to send a request to the Flask server (to trigger the Python script)
void executePythonScript() {
    WiFiClient client;
    HTTPClient http;
    http.begin(client, "http://192.168.1.86:5000/play");  // IP of your Flask server
    int httpCode = http.POST("");  // Send an empty POST request

    if (httpCode == 200) {
        Serial.println("Successfully triggered Python script.");
    } else {
        Serial.println("Failed to trigger Python script.");
    }
    
    http.end();
}

void setup() {
    Serial.begin(115200);  // Debugging output
    Serial1.begin(9600);   // Serial1 (TX on GPIO2) for Python script communication

    Serial.println("Starting ESP8266...");
    
    // Connect to Wi-Fi
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    unsigned long startAttemptTime = millis();
    while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < 15000) { // 15s timeout
        delay(500);
        Serial.print(".");
    }

    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\nWiFi connected. IP address: " + WiFi.localIP().toString());
    } else {
        Serial.println("\nFailed to connect to WiFi.");
        return;
    }

    // Serve HTML page
    server.on("/", HTTP_GET, []() {
        Serial.println("Serving main web page...");
        server.send(200, "text/html", R"rawliteral(
            <html>
                <body>
                    <h1>ESP8266 Vibration Control</h1>
                    <button onclick="sendCommand('play')">Play</button>
                    <button onclick="sendCommand('stop')">Stop</button>
                    <p id="status">Status: Ready</p>
                    <script>
                        function sendCommand(cmd) {
                            fetch('/' + cmd, { method: 'POST' })
                                .then(response => response.text())
                                .then(data => document.getElementById('status').innerText = "Status: " + data);
                        }
                    </script>
                </body>
            </html>
        )rawliteral");
    });

    // Play endpoint: triggers Python script
    server.on("/play", HTTP_POST, []() {
        Serial.println("Received /play request.");
        executePythonScript();  // Run the script on the Flask server

        // Wait for vibration data from the Python script
        Serial.println("Waiting for vibration data...");
        String vibrationData = "";
        unsigned long startTime = millis();
        while (millis() - startTime < 2000) {  // 2s timeout for response
            while (Serial1.available()) {
                char c = Serial1.read();
                vibrationData += c;
            }
        }

        if (vibrationData.length() > 0) {
            Serial.print("Received Vibration Data: ");
            Serial.println(vibrationData);
            server.send(200, "text/plain", "Playing... Vibration: " + vibrationData);
        } else {
            Serial.println("Warning: No vibration data received!");
            server.send(200, "text/plain", "Playing... but no vibration data received.");
        }
    });

    // Stop endpoint: sends STOP command to Python
    server.on("/stop", HTTP_POST, []() {
        Serial.println("Received /stop request.");
        Serial1.println("STOP");  // Tell Python script to stop
        server.send(200, "text/plain", "Stopped.");
    });

    server.begin();
    Serial.println("Web server started.");
}

void loop() {
    server.handleClient();  // Handle incoming client requests
}
