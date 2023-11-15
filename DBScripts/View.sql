create or replace view staff_master_view as
SELECT STAFF_ID,
    STAFF_NAME,
    USERNAME,
    GENDER,
    DOB,
    MOBILE_NO,
    EMAIL_ID,
    JOINING_DATE,
    LEAVING_DATE,
    ACTIVE_STATUS,
    EMPLOYEE_ID,
    PASSWORD,
    STAFF_ROLE_ID,
    roles.role_name
FROM campus_surveillance.staff_master, campus_surveillance.roles
WHERE staff_master.STAFF_ROLE_ID= roles.role_id;