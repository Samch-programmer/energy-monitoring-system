-- MySQL schema for Energy Monitoring System

CREATE DATABASE IF NOT EXISTS energy_monitoring;
USE energy_monitoring;

-- Machines table
CREATE TABLE IF NOT EXISTS Machines (
  machine_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  location VARCHAR(100),
  capacity_kw FLOAT DEFAULT 0.0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users table (for basic auth; passwords should be hashed in production)
CREATE TABLE IF NOT EXISTS Users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('admin','user') DEFAULT 'user',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Energy readings
CREATE TABLE IF NOT EXISTS EnergyReadings (
  reading_id INT AUTO_INCREMENT PRIMARY KEY,
  machine_id INT NOT NULL,
  voltage FLOAT NOT NULL,
  current FLOAT NOT NULL,
  power FLOAT NOT NULL,       -- watts (voltage * current)
  energy_kwh FLOAT NOT NULL,  -- cumulative or per-sample converted measure
  timestamp DATETIME NOT NULL,
  CONSTRAINT fk_machine_reading FOREIGN KEY (machine_id) REFERENCES Machines(machine_id) ON DELETE CASCADE
);

-- Alerts
CREATE TABLE IF NOT EXISTS Alerts (
  alert_id INT AUTO_INCREMENT PRIMARY KEY,
  machine_id INT NOT NULL,
  message VARCHAR(255) NOT NULL,
  alert_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  is_resolved BOOLEAN DEFAULT FALSE,
  CONSTRAINT fk_machine_alert FOREIGN KEY (machine_id) REFERENCES Machines(machine_id) ON DELETE CASCADE
);

-- View: daily energy summary
CREATE OR REPLACE VIEW DailyEnergySummary AS
SELECT
  m.machine_id, m.name,
  DATE(e.timestamp) AS date,
  SUM(e.energy_kwh) AS total_energy_kwh,
  AVG(e.power) AS avg_power_w,
  MAX(e.power) AS peak_power_w
FROM EnergyReadings e
JOIN Machines m ON e.machine_id = m.machine_id
GROUP BY m.machine_id, DATE(e.timestamp);

-- Example indexes for faster queries
CREATE INDEX idx_energy_timestamp ON EnergyReadings(timestamp);
CREATE INDEX idx_energy_machine ON EnergyReadings(machine_id);
