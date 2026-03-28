from flask import Flask, render_template, jsonify, request
import RPi.GPIO as GPIO
from datetime import datetime
import threading
import atexit
import time

app = Flask(__name__)

# GPIO setup
IR_PIN = 17
RELAY_PIN = 27
RELAY_ACTIVE_HIGH = False

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.HIGH)

# Global state
car_count = 0
relay_on = False
battery_voltage = 0.0
display_voltage = 0.0
car_present = False
log = []
lock = threading.Lock()
initialized = False

def log_event(event):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with lock:
        log.append({"time": now, "event": event})
        if len(log) > 50:
            log.pop(0)

def update_relay(state):
    global relay_on
    with lock:
        relay_on = state
        GPIO.output(RELAY_PIN, GPIO.HIGH if (state == RELAY_ACTIVE_HIGH) else GPIO.LOW)

def ir_callback(channel):
    global car_count, initialized, car_present, battery_voltage, display_voltage
    time.sleep(0.05)
    if not initialized:
        initialized = True
        log_event("IR sensor initialized, skipping first read.")
        return

    if GPIO.input(IR_PIN) == GPIO.LOW:
        car_present = True
        car_count += 1
        log_event(f"Car detected. Count: {car_count}")
        if battery_voltage < 4.0:
            update_relay(True)
        else:
            log_event(f"Battery at {battery_voltage:.2f}V, blocking charge")
            update_relay(False)
    else:
        car_present = False
        display_voltage = 0.0
        log_event("Car left")
        update_relay(False)

GPIO.remove_event_detect(IR_PIN)
GPIO.add_event_detect(IR_PIN, GPIO.BOTH, callback=ir_callback, bouncetime=300)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    with lock:
        shown_voltage = display_voltage if car_present else 0.0
        return jsonify({
            "battery_voltage": shown_voltage,
            "battery_percent": int((shown_voltage / 5.0) * 100),
            "relay_status": "CHARGING" if relay_on else "NOT CHARGING",
            "car_count": car_count,
            "log": log
        })

@app.route('/update', methods=['POST'])
def update():
    global battery_voltage, display_voltage
    data = request.get_json()
    if 'battery_voltage' in data:
        try:
            battery_voltage = float(data['battery_voltage'])
            if car_present:
                display_voltage = battery_voltage

            if battery_voltage >= 4.0:
                update_relay(False)
                log_event(f"Battery full at {battery_voltage:.2f}V, stopping charging")
            elif car_present:
                update_relay(True)
                log_event(f"Charging: Battery at {battery_voltage:.2f}V")
        except ValueError:
            return jsonify({"error": "Invalid voltage"}), 400
    return jsonify({"status": "OK"})

def clean_exit():
    GPIO.cleanup()
atexit.register(clean_exit)

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        clean_exit()
