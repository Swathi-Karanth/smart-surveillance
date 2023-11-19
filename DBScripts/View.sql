
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
    BASIC_SALARY 	,
HRA	,
PF	,
TAX_RATE ,
    roles.role_name
FROM campus_surveillance.staff_master INNER JOIN campus_surveillance.roles
ON staff_master.STAFF_ROLE_ID= roles.role_id;

---------------------------------------------------------------------------------------------------

create view footage_view as
select FOOTAGE_ID , recorded_date ,video, cctv.cctv_location,cctv.CCTV_ID 
from footage INNER JOIN cctv on cctv.cctv_id = footage.cctv_id
