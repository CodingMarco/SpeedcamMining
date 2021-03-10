CREATE TABLE speedcams (
  content BIGINT PRIMARY KEY NOT NULL,
  internal_id BIGINT UNIQUE NOT NULL AUTO_INCREMENT,
  lat DECIMAL(8, 6) NOT NULL,
  lng DECIMAL(8, 6) NOT NULL,
  backend VARCHAR(20) NOT NULL,
  id BIGINT,
  country CHAR(2),
  type TINYINT,
  vmax SMALLINT,
  counter SMALLINT,
  created_date DATETIME,
  confirmed_date DATETIME,
  removed_date DATETIME,
  partly_fixed BOOLEAN,
  reason VARCHAR(200)
) ENGINE = InnoDB;
