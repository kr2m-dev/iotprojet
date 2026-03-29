#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid     = "Wokwi-GUEST";
const char* password = "";
const char* serverURL = "http://xmbrk.alwaysdata.net/eau/insert.php";

float ph          = 7.2;
float turbidite   = 1.5;
float temperature = 26.0;
int   direction   = 1;

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("--- Démarrage capteur eau (ESP32) ---");

  WiFi.begin(ssid, password);
  Serial.print("Connexion WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi OK ! IP : " + WiFi.localIP().toString());
}

void loop() {
  ph          += direction * 0.1;
  turbidite   += direction * 0.2;
  temperature += direction * 0.3;
  if (ph > 8.0 || ph < 6.8) direction *= -1;

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    String body = "point_id=forage1";
    body += "&ph="          + String(ph, 2);
    body += "&turbidite="   + String(turbidite, 2);
    body += "&temperature=" + String(temperature, 2);

    Serial.println("Envoi -> " + body);
    int code = http.POST(body);

    if (code > 0) {
      Serial.println("Reponse (" + String(code) + ") : " + http.getString());
    } else {
      Serial.println("Erreur : " + http.errorToString(code));
    }
    http.end();
  }

  delay(10000);
}