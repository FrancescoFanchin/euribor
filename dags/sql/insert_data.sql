CREATE TABLE IF NOT EXISTS euribor2(
  euribor_id uuid NOT NULL DEFAULT gen_random_uuid(),
  time_period varchar(10) NOT NULL,
  obs_value decimal NOT NULL,
  PRIMARY KEY (euribor_id)
);

INSERT INTO euribor2 (time_period, obs_value) VALUES
