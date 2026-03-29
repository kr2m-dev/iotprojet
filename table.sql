CREATE TABLE mesures_eau (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  point_id   VARCHAR(50)  NOT NULL DEFAULT 'forage1',
  ph         FLOAT        NOT NULL,
  turbidite  FLOAT        NOT NULL,
  temperature FLOAT       NOT NULL,
  alerte     TINYINT(1)   NOT NULL DEFAULT 0,
  created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);