import time
import random
from datetime import datetime
import requests

URL = "http://127.0.0.1:5000/api/readings"

machines = [
    {"machine_id": 1, "name": "Pump A"},
    {"machine_id": 2, "name": "Compressor B"},
    {"machine_id": 3, "name": "Motor C"},
]

while True:
    for m in machines:
        voltage = random.uniform(210, 240)
        current = random.uniform(5, 15)
        energy_kwh = (voltage * current) / 1000.0
        data = {
            "machine_id": m["machine_id"],
            "voltage": voltage,
            "current": current,
            "energy_kwh": energy_kwh,
            "timestamp": datetime.utcnow().isoformat()
        }
        try:
            requests.post(URL, json=data)
            print(f"Added reading for {m['name']} - {voltage:.1f}V {current:.1f}A")
        except Exception as e:
            print("Error:", e)
    time.sleep(5)
