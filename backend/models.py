# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Machine(db.Model):
    __tablename__ = 'Machines'  # match exact table name
    machine_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    capacity_kw = db.Column(db.Float)

    readings = db.relationship('EnergyReading', backref='machine', lazy=True)
    alerts = db.relationship('Alert', backref='machine', lazy=True)


class EnergyReading(db.Model):
    __tablename__ = 'EnergyReadings'  # match exact table name
    reading_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('Machines.machine_id'), nullable=False)
    voltage = db.Column(db.Float, nullable=False)
    current = db.Column(db.Float, nullable=False)
    power = db.Column(db.Float)
    energy_kwh = db.Column(db.Float, default=0.0)
    timestamp = db.Column(db.DateTime, nullable=False)


class Alert(db.Model):
    __tablename__ = 'Alerts'  # match exact table name
    alert_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('Machines.machine_id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    alert_time = db.Column(db.DateTime, nullable=False)
    is_resolved = db.Column(db.Boolean, default=False)


class DailyEnergySummary(db.Model):
    __tablename__ = 'DailyEnergySummary'
    summary_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    machine_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    total_energy_kwh = db.Column(db.Float, default=0.0)
    avg_power_w = db.Column(db.Float, default=0.0)
    peak_power_w = db.Column(db.Float, default=0.0)


class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50))
