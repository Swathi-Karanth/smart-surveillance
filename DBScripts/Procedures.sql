
--STAFF_DATA ANALYSIS PROCEDURE
--test cases
-- Query max aged staff
call staff_data_analysis(null, null, 'MAX',NULL,NULL)

-- query min aged staff
call staff_data_analysis(null, null, 'MIN',NULL,NULL)

-- query staff based on age range
call staff_data_analysis(null, null, null,30,40)

-- query based on joining date
call staff_data_analysis('2015-01-01','2016-12-31', null,null,null)

DELIMITER //

CREATE  PROCEDURE staff_data_analysis (join_from_date varchar(100), join_to_date varchar(100),
age_condition varchar(10), age_range_from int, age_range_to int)

begin
IF age_condition ='MAX' then

SELECT STAFF_ID, STAFF_NAME,USERNAME, GENDER, DOB
FROM staff_master
WHERE DOB = (
    SELECT MIN(DOB)
    FROM staff_master
);
END IF;

IF age_condition ='MIN' then

SELECT STAFF_ID, STAFF_NAME, USERNAME,GENDER, DOB
FROM staff_master
WHERE DOB = (
    SELECT MAX(DOB)
    FROM staff_master
);
END IF;

if age_range_from is not null and age_range_to is not null then

SELECT STAFF_ID, STAFF_NAME, GENDER, DOB, TIMESTAMPDIFF(YEAR, DOB, CURDATE()) as age
FROM staff_master
WHERE TIMESTAMPDIFF(YEAR, DOB, CURDATE()) >= age_range_from and TIMESTAMPDIFF(YEAR, DOB, CURDATE()) <= age_range_to
order by 5;

end if;

if join_from_date is not null and  join_to_date is not null then

SELECT STAFF_ID, STAFF_NAME, USERNAME,GENDER, DOB, date(JOINING_DATE) as joindate
FROM staff_master
where 
 date(JOINING_DATE) >= STR_TO_DATE(join_from_date , "%Y-%m-%d")
and date(JOINING_DATE) <= STR_TO_DATE(join_to_date, "%Y-%m-%d")
order by date(JOINING_DATE);
end if;

END //

--------------------------------------------------------------------------------------------------------------

--AUDITQUERYPROCEDURE


DELIMITER //
CREATE PROCEDURE AUDITLOGREPORT(p_tablename varchar(200), fromdate varchar(100), todate varchar(100))
BEGIN
 
SELECT *  FROM audit_change_history WHERE AUDIT_TABLE_NAME =p_tablename 
and date(dml_timestamp) >= STR_TO_DATE(fromdate,"%Y-%m-%d")
and date(dml_timestamp) <= STR_TO_DATE(todate,"%Y-%m-%d")

END //

--test case
call AUDITLOGREPORT('ROLES','2023-10-28','2023-10-28')


