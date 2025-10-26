from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Machine, EnergyReading, Alert
from db_config import SQLALCHEMY_DATABASE_URI
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/api/readings/latest")
def latest_readings():
    readings = (
        db.session.query(EnergyReading, Machine.name)
        .join(Machine, EnergyReading.machine_id == Machine.id)
        .order_by(EnergyReading.timestamp.desc())
        .limit(10)
        .all()
    )
    return jsonify([
        {
            "machine_id": r.EnergyReading.machine_id,
            "name": r.name,
            "voltage": r.EnergyReading.voltage,
            "current": r.EnergyReading.current,
            "power": r.EnergyReading.power,
            "energy_kwh": r.EnergyReading.energy_kwh,
            "timestamp": r.EnergyReading.timestamp.isoformat(),
        }
        for r in readings
    ])

@app.route("/api/readings/summary")
def summary():
    hours = int(request.args.get("hours", 24))
    since = datetime.utcnow() - timedelta(hours=hours)
    readings = EnergyReading.query.filter(EnergyReading.timestamp >= since).all()
    if not readings:
        return jsonify({"avg_power_w": 0, "peak_power_w": 0, "total_energy_kwh": 0})
    avg_power = sum(r.power for r in readings) / len(readings)
    peak_power = max(r.power for r in readings)
    total_energy = sum(r.energy_kwh for r in readings)
    return jsonify({
        "avg_power_w": avg_power,
        "peak_power_w": peak_power,
        "total_energy_kwh": total_energy,
    })

@app.route("/api/alerts")
def get_alerts():
    alerts = Alert.query.order_by(Alert.alert_time.desc()).limit(10).all()
    return jsonify([
        {
            "machine_id": a.machine_id,
            "message": a.message,
            "alert_time": a.alert_time.isoformat(),
        }
        for a in alerts
    ])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)