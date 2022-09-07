USE peter_park_plate_db;

CREATE TABLE IF NOT EXISTS `tblLicensePlates` (
    `ID` int not null AUTO_INCREMENT,
    `Plate` VARCHAR(10) not null,
    `DateCreated` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY `PK_tblLicencePlaces` (`ID`),
    UNIQUE KEY 'UQ_tblLicencePlaces_Plate' (`Plate`)
) ENGINE=INNODB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;



