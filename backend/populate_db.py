# populate_db.py
from app import app, db
from models import Machine, EnergyReading, Alert
from datetime import datetime
import random

with app.app_context():
    # Add machines
    if not Machine.query.first():
        m1 = Machine(name="Compressor A", location="Factory 1", capacity_kw=50)
        m2 = Machine(name="Pump B", location="Factory 2", capacity_kw=30)
        db.session.add_all([m1, m2])
        db.session.commit()
        print("Machines added")

    # Add readings
    machines = Machine.query.all()
    for m in machines:
        for i in range(5):  # 5 readings per machine
            voltage = random.uniform(210, 240)
            current = random.uniform(5, 20)
            power = voltage * current
            energy_kwh = power / 1000 * 1  # 1 hour assumption
            r = EnergyReading(
                machine_id=m.machine_id,
                voltage=voltage,
                current=current,
                power=power,
                energy_kwh=energy_kwh,
                timestamp=datetime.utcnow()
            )
            db.session.add(r)
    db.session.commit()
    print("Energy readings added")
