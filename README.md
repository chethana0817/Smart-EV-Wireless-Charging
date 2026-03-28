🚗 Software Controlled Wireless Power Transmission

📌 Overview

This project implements a **Smart EV Wireless Charging System** using ESP32 and Raspberry Pi.
The system automatically detects a vehicle, starts wireless charging, continuously monitors battery voltage, and **automatically turns off charging when the battery is fully charged**, ensuring safety and efficiency.

---

⚙️ Features

* 🔍 Automatic vehicle detection using IR sensor
* ⚡ Wireless charging control using relay
* 🔋 Real-time battery voltage monitoring (ESP32)
* 📊 Live dashboard using Flask (Raspberry Pi)
* 🧠 Automatic cutoff when battery reaches full charge (4.0V)
* 📈 Battery percentage display
* 📝 Event logging system

---

🛠️ Technologies Used

* ESP32
* Raspberry Pi
* Python (Flask)
* HTML, CSS, JavaScript
* IR Sensor & Relay

---

🔄 Working Principle

1. 🚗 IR sensor detects the vehicle
2. ⚡ Relay turns ON → Charging starts
3. 🔋 ESP32 reads battery voltage
4. 🌐 Sends data to Raspberry Pi
5. 📊 Dashboard updates in real-time
6. 🛑 Charging turns OFF automatically when battery is full (4.0V)

---

📂 Project Structure

```
Smart-EV-Wireless-Charging/
│
├── esp32/
│   └── ESP_CODE.ino
│
├── app.py
│
├── templates/
│   └── index.html
│
├── README.md


---

🚀 Setup Instructions

### 🔹 Raspberry Pi

```bash
pip install flask
python3 app.py
```

---

### 🔹 ESP32

* Update WiFi credentials
* Set Raspberry Pi IP
* Upload code

---

📊 Dashboard

* Live voltage monitoring
* Charging status display
* Car detection tracking

---


🎯 Applications

* Smart EV charging systems
* IoT automation projects
* Wireless power transmission

---

👩‍💻 Author

**Chethana**
