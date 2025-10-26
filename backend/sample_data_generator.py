# sample_data_generator.py
import requests, time, random, os
from datetime import datetime

API_BASE = os.getenv('API_BASE', 'http://127.0.0.1:5000/api')

MACHINE_IDS = [1, 2] 
def generate_reading(mid):
   
    voltage = random.uniform(210, 240)
   
    current = random.uniform(1.0, 30.0)
    power = voltage * current
   
    energy_kwh = power * (1/60) / 1000.0
    payload = {
        'machine_id': mid,
        'voltage': voltage,
        'current': current,
        'energy_kwh': round(energy_kwh, 6),
        'timestamp': datetime.utcnow().isoformat()
    }
    return payload

def main():
    print("Starting sample data generator. Press Ctrl+C to stop.")
    while True:
        for mid in MACHINE_IDS:
            try:
                payload = generate_reading(mid)
                r = requests.post(f"{API_BASE}/readings", json=payload, timeout=5)
                print("Posted", payload, "->", r.status_code, r.text)
            except Exception as e:
                print("Error:", e)
        time.sleep(10)
if __name__ == '__main__':
    main()
