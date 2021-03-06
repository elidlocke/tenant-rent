PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE tenants (
user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
email TEXT NOT NULL );
INSERT INTO tenants VALUES(2,'Joe Smith','joe@test.com');
INSERT INTO tenants VALUES(3,'John Smith','john@test.com');
INSERT INTO tenants VALUES(5,'Mary Smith','mary_smith@test.com');
INSERT INTO tenants VALUES(6,'May Smith','may_smith@test.com');
INSERT INTO tenants VALUES(9,'M Smith','m@test.com');
INSERT INTO tenants VALUES(10,'Tracy Meng','tcmeng@gmail.com');
INSERT INTO tenants VALUES(11,'Tracy Meng','tcmeng@gmail.com');
INSERT INTO tenants VALUES(12,'Sarah Summers','sarahsummers@gmail.com');
INSERT INTO tenants VALUES(13,'Samantha Dollier','samantha@dollier.com');
INSERT INTO tenants VALUES(14,'Joe Smith','joe@smith.com');
INSERT INTO tenants VALUES(15,'John Doer','johndoer@gmail.com');
INSERT INTO tenants VALUES(16,'Gearge Thompson','george@thompson.com');
INSERT INTO tenants VALUES(17,'Angie Mwangalle','bethnenniger+angie@gmail.com');
INSERT INTO tenants VALUES(18,'Bob Bob','bethnenniger+bob@gmail.com');
INSERT INTO tenants VALUES(19,'May May','bethnenniger@maymay.com');
INSERT INTO tenants VALUES(20,'3','sd');
CREATE TABLE rooms(
room_id CHAR(1) PRIMARY KEY NOT NULL,
rentable INT NOT NULL , price INTEGER NOT NULL DEFAULT 0);
INSERT INTO rooms VALUES('A',1,595);
INSERT INTO rooms VALUES('B',0,0);
INSERT INTO rooms VALUES('C',0,0);
INSERT INTO rooms VALUES('D',1,595);
INSERT INTO rooms VALUES('E',1,595);
INSERT INTO rooms VALUES('F',1,545);
INSERT INTO rooms VALUES('G',1,545);
INSERT INTO rooms VALUES('H',1,545);
INSERT INTO rooms VALUES('I',1,595);
INSERT INTO rooms VALUES('J',1,545);
INSERT INTO rooms VALUES('K',1,595);
CREATE TABLE IF NOT EXISTS "rent" (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
room_id CHAR(1) NOT NULL,
date TEXT NOT NULL,
paid INTEGER NOT NULL,
receipt_issued INTEGER NOT NULL DEFAULT 0, receipt_sent INTEGER NOT NULL DEFAULT 0);
INSERT INTO rent VALUES(11,3,'B','2018-09-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(12,3,'B','2018-10-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(13,3,'B','2018-11-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(14,3,'B','2018-12-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(15,10,'A','2018-09-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(16,10,'A','2018-10-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(17,10,'A','2018-11-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(18,10,'A','2018-12-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(19,10,'A','2018-01-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(20,10,'A','2018-02-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(21,10,'A','2018-03-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(22,10,'A','2018-04-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(31,12,'D','2018-09-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(32,12,'D','2018-10-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(33,12,'D','2018-11-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(34,12,'D','2018-12-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(35,15,'D','2018-05-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(36,15,'D','2018-06-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(37,15,'D','2018-07-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(38,15,'D','2018-08-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(39,16,'H','2018-09-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(40,16,'H','2018-10-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(41,16,'H','2018-11-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(42,16,'H','2018-12-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(43,16,'D','2017-09-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(44,16,'D','2017-10-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(45,16,'D','2017-11-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(46,16,'D','2017-12-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(47,6,'J','2018-09-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(48,6,'J','2018-10-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(49,6,'J','2018-11-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(50,6,'J','2018-12-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(51,13,'I','2018-09-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(52,13,'I','2018-10-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(53,13,'I','2018-11-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(54,13,'I','2018-12-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(55,10,'K','2018-09-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(56,10,'K','2018-10-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(57,10,'K','2018-11-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(58,10,'K','2018-12-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(59,17,'D','2019-01-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(60,17,'D','2019-02-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(61,17,'D','2019-03-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(62,17,'D','2019-04-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(63,18,'F','2019-01-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(64,18,'F','2019-02-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(65,18,'F','2019-03-01 00:00:00',1,1,1);
INSERT INTO rent VALUES(66,18,'F','2019-04-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(67,19,'H','2019-01-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(68,19,'H','2019-02-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(69,19,'H','2019-03-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(70,19,'H','2019-04-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(71,19,'A','2020-01-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(72,19,'A','2020-02-01 00:00:00',0,0,0);
INSERT INTO rent VALUES(73,19,'A','2020-03-01 00:00:00',1,0,0);
INSERT INTO rent VALUES(74,19,'A','2020-04-01 00:00:00',1,1,1);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('tenants',20);
INSERT INTO sqlite_sequence VALUES('rent',74);
COMMIT;
