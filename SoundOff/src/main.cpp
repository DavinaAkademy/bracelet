#include <ESP8266WiFi.h>

const char *ssid = "ITAKADEMY-STUDENTS";
const char *password = "itakademy";

// ESP8266 IP and port
WiFiServer server(12345);  // Same port as in your Flask server

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  server.begin();  // Start the server
}

void loop() {
  WiFiClient client = server.available();  // Listen for incoming clients

  if (client) {
    Serial.println("Client connected");
    String vibrationData = "";

    // Read the data sent from the Flask server
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();  // Read the incoming byte
        vibrationData += c;  // Append to the vibration data
        delay(5);
        
        if (c == '\n') {  // End of data transmission (newline character)
          Serial.print("Received vibration data: ");
          Serial.println(vibrationData);
          
          // Parse and process the vibration data here if needed
          int vibrationIntensity = vibrationData.toInt();
          if (vibrationIntensity > 0) {
            // Control the vibration motor using PWM (for example)
            analogWrite(5, vibrationIntensity);
          }
          vibrationData = "";  // Reset data for next transmission
        }
      }
    }
    client.stop();  // Disconnect the client after the transmission is complete
    Serial.println("Client disconnected");
  }
}
