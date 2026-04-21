CREATE TABLE IF NOT EXISTS resety (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(255),
    token VARCHAR(255),
    data_czas INT
);

CREATE TABLE IF NOT EXISTS turnieje_europejskie (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazwa VARCHAR(255) NOT NULL,
    kraj VARCHAR(255) NOT NULL,
    data VARCHAR(255) NOT NULL,
    zwyciezca VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS turnieje_krajowe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazwa VARCHAR(255) NOT NULL,
    data VARCHAR(255) NOT NULL,
    zwyciezca VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS uzytkownicy (
    login VARCHAR(255) PRIMARY KEY,
    haslo VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    zespol VARCHAR(255) NOT NULL,
    reset_token VARCHAR(255),
    reset_ts INT
);

INSERT INTO uzytkownicy VALUES ('adi','adi123','lourfix01@gmail.com','NetłorkCherołs',NULL,NULL);
INSERT INTO uzytkownicy VALUES ('adi2','adi123','adi@gmail.com','NetłorkCherołs',NULL,NULL);
INSERT INTO uzytkownicy VALUES ('adi3','adi123','adi3@gmail.com','NetłorkCherołs',NULL,NULL);
INSERT INTO uzytkownicy VALUES ('adi4','adi123','adi4@gmail.com','NetłorkCherołs',NULL,NULL);
INSERT INTO uzytkownicy VALUES ('adi5','adi123','adi5@wp.pl','1',NULL,NULL);
