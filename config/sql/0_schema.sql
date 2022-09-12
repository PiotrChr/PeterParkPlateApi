USE peter_park_plate_db;

CREATE TABLE IF NOT EXISTS `tblLicensePlates` (
    `ID` int not null AUTO_INCREMENT,
    `Plate` VARCHAR(10) NOT NULL,
    `DateCreated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY `PK_tblLicencePlaces` (`ID`)
) ENGINE=INNODB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
