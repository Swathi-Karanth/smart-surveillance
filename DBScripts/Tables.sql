create schema campus_surveillance;
use campus_surveillance;
CREATE TABLE STAFF_MASTER (
STAFF_ID		int NOT NULL AUTO_INCREMENT PRIMARY KEY,
STAFF_NAME		varchar(255) NOT NULL,
USERNAME 		varchar(100) NOT NULL,
GENDER			varchar(1) NOT NULL,
DOB				DATE NOT NULL,
MOBILE_NO		varchar(20) NOT NULL,
EMAIL_ID		varchar(50) ,
JOINING_DATE	DATE NOT NULL ,
LEAVING_DATE	DATE ,
ACTIVE_STATUS	varchar(1) NOT NULL,
EMPLOYEE_ID		varchar(20) NOT NULL,
PASSWORD		varchar(20)  NULL,
STAFF_ROLE_ID			int, 
FOREIGN KEY (STAFF_ROLE) REFERENCES ROLES(ROLE_ID));

CREATE TABLE ROLES (
	ROLE_ID		int PRIMARY KEY,
	ROLE_NAME	varchar(255) NOT NULL);
ALTER TABLE ROLES AUTO_INCREMENT=100;


ALTER TABLE STAFF_MASTER AUTO_INCREMENT=100;

ALTER TABLE STAFF_MASTER ADD CONSTRAINT gender_cons CHECK (GENDER IN ('M', 'F', 'O'));

CREATE TABLE DUTY_ROSTER(
STAFF_SHIFT_ID	int NOT NULL AUTO_INCREMENT PRIMARY KEY,
STAFF_ID		INT NOT NULL,
 FOREIGN KEY (STAFF_ID) REFERENCES STAFF_MASTER(STAFF_ID),
SHIFT_ID		INT NOT NULL,
 FOREIGN KEY(SHIFT_ID) REFERENCES SHIFT_MASTER(SHIFT_ID),
START_DATE_TIME	DATE NOT NULL,
END_DATE_TIME	DATE );

ALTER TABLE DUTY_ROSTER AUTO_INCREMENT=100;

CREATE TABLE SHIFT_MASTER (
	SHIFT_ID	int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	SHIFT_NAME	varchar(255) NOT NULL,
	START_TIME	varchar(50) NOT NULL,
	END_TIME	varchar(50) NOT NULL
	);	

ALTER TABLE SHIFT_MASTER AUTO_INCREMENT=100;

CREATE TABLE INCIDENT_TYPES(
INC_TYPE_ID		int NOT NULL AUTO_INCREMENT PRIMARY KEY,
INCIDENT_TYPE	VARCHAR(50) NOT NULL );

ALTER TABLE INCIDENT_TYPES AUTO_INCREMENT=100;

CREATE TABLE INCIDENTS(
INCIDENT_ID			int NOT NULL AUTO_INCREMENT PRIMARY KEY,
INCIDENT_TYPE_ID	INT ,
FOREIGN KEY (INCIDENT_TYPE_ID) REFERENCES INCIDENT_TYPES(INC_TYPE_ID),
INCIDENT_DESC		VARCHAR(500),
REPORTED_STAFF_ID	INT ,
FOREIGN KEY (REPORTED_STAFF_ID) REFERENCES STAFF_MASTER(STAFF_ID), -- details recorded by which staff
REPORTED_DATE_TIME	DATETIME NOT NULL,
ACTION				VARCHAR(500) NOT NULL,
STATUS				VARCHAR(1) NOT NULL );

ALTER TABLE INCIDENTS ADD CONSTRAINT status_cons CHECK (STATUS IN ('C','O'));

CREATE TABLE VISITOR_LEDGER(
VISITOR_ID			Int NOT NULL AUTO_INCREMENT PRIMARY KEY,
DATE_TIME			DATETIME  NOT NULL ,
VISITOR_NAME		VARCHAR(100)  NOT NULL,
PURPOSE_OF_VISIT	VARCHAR(100)  NOT NULL,
ENTRY_DATE_TIME		DATETIME NOT NULL,
EXIT_DATE_TIME		DATETIME,
VISITOR_CONTACT		VARCHAR(20) NOT NULL,
RECORDED_BY_ID		int  NOT NULL ,
FOREIGN KEY (RECORDED_BY_ID) REFERENCES STAFF_MASTER(STAFF_ID)); -- details recorded by which staff

ALTER TABLE VISITOR_LEDGER AUTO_INCREMENT=100;

CREATE TABLE EMERGENCY_CONTACTS(
e_id			Int NOT NULL AUTO_INCREMENT PRIMARY KEY,
TYPE		VARCHAR(100) NOT NULL,
ADDRESS		VARCHAR(200) NOT NULL,	
CONTACT_NO	VARCHAR(20),	
GOOGLE_MAP_LINK	VARCHAR(1000) ) ;

ALTER TABLE EMERGENCY_CONTACTS AUTO_INCREMENT=100;

CREATE TABLE CCTV(
CCTV_ID INT PRIMARY KEY,
CCTV_LOCATION VARCHAR(50),
MODEL VARCHAR(50)
);

ALTER TABLE CCTV AUTO_INCREMENT=100;

CREATE TABLE FOOTAGE(
FOOTAGE_ID INT PRIMARY KEY auto_increment,
recorded_date TIMESTAMP,
video_folder VARCHAR(500) ,
video longblob,
CCTV_ID INT,
FOREIGN KEY (CCTV_ID) REFERENCES CCTV(CCTV_ID));

ALTER TABLE FOOTAGE AUTO_INCREMENT=100;

CREATE TABLE audit_change_history (
    audit_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    parent_table_pk BIGINT NOT NULL,
    old_row_data JSON,
    new_row_data JSON,
    dml_type ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    dml_timestamp DATETIME NOT NULL,
    audit_table_name varchar(255));
    
ALTER TABLE audit_change_history AUTO_INCREMENT=100;

CREATE USER 'MichaelJohnson'@'localhost' IDENTIFIED BY 'pass123';
GRANT SELECT,INSERT ON campus_surveillance.staff_master TO 'MichaelJohnson'@'localhost';
GRANT SELECT ON campus_surveillance.incidents TO 'MichaelJohnson'@'localhost';
REVOKE INSERT ON campus_surveillance.incidents FROM 'MichaelJohnson'@'localhost';


-- sample video insert query with longblob

-- INSERT INTO footage (video_folder, recorded_date, video,CCTV_ID) 
-- values ('E:\DUMPYARD\PESU Files\Semester 5\DBMS\MiniProject\code_start\SmartSurveillance_mySQL\SmartSurveillance_mySQL\Django-CRM-main\website\cctv_footage_sample',
-- SYSDATE(),
-- LOAD_FILE("E:\DUMPYARD\PESU Files\Semester 5\DBMS\MiniProject\code_start\SmartSurveillance_mySQL\SmartSurveillance_mySQL\Django-CRM-main\website\cctv_footage_sample\vid2.mp4"),
-- 101);