
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

SELECT STAFF_ID, STAFF_NAME, GENDER, DOB, TIMESTAMPDIFF(YEAR, DOB, CURDATE()) as AGE
FROM staff_master
WHERE DOB = (
    SELECT MIN(DOB)
    FROM staff_master
);
END IF;

IF age_condition ='MIN' then

SELECT STAFF_ID, STAFF_NAME,GENDER, DOB, TIMESTAMPDIFF(YEAR, DOB, CURDATE()) as AGE
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

SELECT STAFF_ID, STAFF_NAME,GENDER, DOB, TIMESTAMPDIFF(YEAR, DOB, CURDATE()) as age,date(JOINING_DATE) as joindate
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

------------------------------------------------------------------------------------------------------------------

-- SALARY GENERATION PROCEDURE
DELIMITER //

CREATE PROCEDURE calculate_salary(p_staff_id INT,  p_MONTH VARCHAR(50),  p_YEAR VARCHAR(50))
BEGIN
    DECLARE L_basic_salary INT;
    DECLARE L_hra INT;
    DECLARE L_pf INT;
    DECLARE L_tax_rate INT;
    DECLARE unpaid_leaves INT;
    DECLARE l_net_salary FLOAT;
	DECLARE p_record_exists INT;
    DECLARE taxable_income FLOAT;
    DECLARE pf_deduction FLOAT;
   DECLARE tax_deduction FLOAT;
    -- Declare variables for exception handling
    DECLARE error_occurred BOOLEAN DEFAULT FALSE;
    DECLARE error_code INT;
    DECLARE error_message VARCHAR(255);

    -- Exception handling
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        SET error_occurred = TRUE;
        GET DIAGNOSTICS CONDITION 1
            error_code = MYSQL_ERRNO, error_message = MESSAGE_TEXT;
        SELECT CONCAT('Error ', error_code, ': ', error_message) AS error;
    END;


    -- Get salary details
    SELECT basic_salary, hra, pf, tax_rate
    INTO L_basic_salary, L_hra, L_pf, L_tax_rate
    FROM STAFF_MASTER
    WHERE STAFF_ID = p_staff_id;


SELECT L_basic_salary, L_hra, L_pf, L_tax_rate;
-- take uplaid leaves


select unpaid_leave INTO unpaid_leaves from STAFF_LEAVE_DETAILS   
WHERE STAFF_ID = p_staff_id and leave_month = p_month and leave_year = p_year ;

IF unpaid_leaves IS NULL THEN 
	SET unpaid_leaves =0;
END IF;

    SET taxable_income = L_basic_salary + L_hra;
    SET pf_deduction = (L_pf / 100) * L_basic_salary;
    SET tax_deduction = (L_tax_rate / 100) * taxable_income;

SELECT 'xx';
SELECT taxable_income,pf_deduction,tax_deduction ;

    -- Calculate net salary considering unpaid leaves
    SET l_net_salary = (L_basic_salary + L_hra) - (pf_deduction + tax_deduction);

select l_net_salary;

	if unpaid_leaves > 0 then
		SET l_net_salary = net_salary - ((L_basic_salary + L_hra) / 30) * unpaid_leaves;
	end if;
    
    -- SET l_net_salary = ROUND(l_net_salary,0); 
    SET p_record_exists = 0;

	
    SELECT COUNT(1) INTO p_record_exists from STAFF_SALARY_DETAILS
   where  STAFF_ID = p_staff_id and salary_month = p_month and salary_year = p_year ;
  
   
   
 if p_record_exists = 0 then
 	INSERT INTO  STAFF_SALARY_DETAILS (STAFF_ID,SALARY_MONTH, SALARY_YEAR, NET_SALARY)
 	VALUES (p_staff_id, p_MONTH, p_YEAR,  ROUND(l_net_salary));
 
 	
    elseif p_record_exists = 1 then
      update STAFF_SALARY_DETAILS
      set net_salary = ROUND(l_net_salary)
      where STAFF_ID = p_staff_id and salary_month = p_month and salary_year = p_year ;

	end if; 
IF error_occurred THEN
        ROLLBACK; -- Rollback any changes in case of an error
	
    ELSE
        COMMIT;   -- Commit changes if no error occurred
   END IF;

END //

--testcase
call calculate_salary(100,'NOV','2023')
