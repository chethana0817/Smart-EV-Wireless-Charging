#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "";
const char* password = "";
const char* serverName = "http://IP_ADDRESS:5000/update";  // Flask endpoint

#define VOLTAGE_PIN 36  // GPIO36

// Voltage divider resistors
const float R1 = 100000.0;
const float R2 = 100000.0;

// ADC settings
const float ADC_MAX = 4095.0;
const float VREF = 3.3;
const float CALIBRATION = 1.145;

int readAverageADC(int pin, int samples = 10) {
  long total = 0;
  for (int i = 0; i < samples; i++) {
    total += analogRead(pin);
    delay(5);
  }
  return total / samples;
}

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi");
}

void loop() {
  int adcValue = readAverageADC(VOLTAGE_PIN);
  float vOut = (adcValue / ADC_MAX) * VREF;
  float batteryVoltage = vOut * ((R1 + R2) / R2) * CALIBRATION;

  Serial.print("ADC: "); Serial.print(adcValue);
  Serial.print(" | Voltage: "); Serial.println(batteryVoltage, 2);

  if (WiFi.status() == WL_CONNECTED && batteryVoltage > 2.0 && batteryVoltage < 6.0) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");
    
    String payload = "{\"battery_voltage\":" + String(batteryVoltage, 2) + "}";
    int httpResponseCode = http.POST(payload);

    Serial.print("HTTP Response: "); Serial.println(httpResponseCode);

    http.end();
  } else {
    Serial.println("Wi-Fi not connected or voltage out of range");
  }

  delay(2000);
}
