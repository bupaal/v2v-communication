#include <WiFi.h>
#include <WebServer.h>
#include <Firebase_ESP_Client.h>

// Wi-Fi credentials
const char* ssid = "vivo Y56 5G";
const char* password = "87654321";

// Firebase credentials
#define FIREBASE_HOST "https://comms-project-27524-default-rtdb.asia-southeast1.firebasedatabase.app/"
#define FIREBASE_AUTH "ZX83opRiRn2f3GXqBfKaVUkqEo2borzxFI0GtL0S"

// Firebase objects
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

WebServer server(80);  // HTTP server on port 80

// Function to handle alerts sent by the Python script
void handleAlert() {
  String carID = server.arg("car");  // Get car ID from request
  String message = server.arg("message");  // Get message from request

  

  // Firebase path for storing alert message
  String path = "/alerts/" + carID + "/message";  

  if (Firebase.RTDB.setString(&fbdo, path.c_str(), message.c_str())) {
    Serial.println("Alert sent to Firebase successfully!");
  } else {
    Serial.println("Firebase Write Error: " + fbdo.errorReason());
  }

  // Respond to the Python script
  server.send(200, "text/plain", "Alert received: " + message);
}

// Function to read messages from Firebase for both Car_A and Car_B
void readAlertMessages() {
  String cars[] = {"Car_A", "Car_B"};
  
  for (int i = 0; i < 2; i++) {
    String carID = cars[i];
    String path = "/alerts/" + carID + "/message";

    if (Firebase.RTDB.getString(&fbdo, path.c_str())) {
      String message = fbdo.stringData();
      

      // Check if Drowsiness is detected
      if (message == "Drowsiness Detected!") {
        Serial.print("ALERT! ");
        Serial.print(carID);
        Serial.println(" detected drowsiness!");
      }
    } else {
      Serial.print("Firebase Read Error for ");
      Serial.print(carID);
      Serial.print(": ");
      Serial.println(fbdo.errorReason());
    }
  }
}

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to Wi-Fi");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());

  // Configure Firebase
  config.database_url = FIREBASE_HOST;
  config.signer.tokens.legacy_token = FIREBASE_AUTH;

  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  // Test Firebase connection
  if (Firebase.RTDB.setString(&fbdo, "/test", "Hello Firebase!")) {
    Serial.println("Firebase test write successful!");
  } else {
    Serial.println("Firebase test failed: " + fbdo.errorReason());
  }

  // Set up the alert route
  server.on("/alert", HTTP_GET, handleAlert);

  // Start the web server
  server.begin();
}

void loop() {
  server.handleClient();  // Listen for incoming HTTP requests

  // Read the latest alert message from Firebase every 5 seconds
  readAlertMessages();
  delay(5000);
}