#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "ITAKADEMY-STUDENTS";
const char* password = "itakademy";

ESP8266WebServer server(80);

// Wi-Fi and Web Server Setup
void setup() {
    Serial.begin(115200);  // Debugging output
    Serial1.begin(9600);   // Use Serial1 (TX on GPIO2) for Python script communication

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

    // Set up web server endpoints
    server.on("/", HTTP_GET, []() {
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

    server.on("/play", HTTP_POST, []() {
        Serial.println("Received /play request.");
        Serial1.println("PLAY");  // Send to Python script

        // Wait for the vibration data from the Python script
        String vibrationData = "";
        unsigned long startTime = millis();
        while (millis() - startTime < 2000) {  // 2s timeout for response
            while (Serial1.available()) {
                char c = Serial1.read();
                vibrationData += c;
            }
        }

        Serial.println("Vibration Data: " + vibrationData);
        server.send(200, "text/plain", "Playing... Vibration: " + vibrationData);
    });

    server.on("/stop", HTTP_POST, []() {
        Serial.println("Received /stop request.");
        Serial1.println("STOP");  // Send stop command to Python script
        server.send(200, "text/plain", "Stopped.");
    });

    server.begin();
    Serial.println("Web server started.");
}

void loop() {
    server.handleClient();  // Handle incoming client requests
}
