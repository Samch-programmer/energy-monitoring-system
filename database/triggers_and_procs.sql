USE energy_monitoring;

-- Trigger to insert alert when power exceeds threshold (80% of capacity_kw * 1000 to convert kW to W)
DELIMITER $$
CREATE TRIGGER trg_power_alert
AFTER INSERT ON EnergyReadings
FOR EACH ROW
BEGIN
  DECLARE cap_kw FLOAT;
  SELECT capacity_kw INTO cap_kw FROM Machines WHERE machine_id = NEW.machine_id;
  IF cap_kw IS NOT NULL AND NEW.power > 0.8 * cap_kw * 1000 THEN
    INSERT INTO Alerts(machine_id, message, alert_time)
    VALUES (NEW.machine_id, CONCAT('High power usage detected: ', ROUND(NEW.power,2), ' W'), NEW.timestamp);
  END IF;
END$$
DELIMITER ;

-- Stored proc: daily summary for given date
DELIMITER $$
CREATE PROCEDURE sp_get_daily_summary(IN ref_date DATE)
BEGIN
  SELECT * FROM DailyEnergySummary WHERE date = ref_date;
END$$
DELIMITER ;
