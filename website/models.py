from pyexpat import model
from django.db import models

class Record(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=50)
	last_name =  models.CharField(max_length=50)
	email =  models.CharField(max_length=100)
	phone = models.CharField(max_length=15)
	address =  models.CharField(max_length=100)
	city =  models.CharField(max_length=50)
	state =  models.CharField(max_length=50)
	zipcode =  models.CharField(max_length=20)

	def __str__(self):
		return(f"{self.first_name} {self.last_name}")

class EMERGENCY_CONTACTS(models.Model):
	e_id = models.AutoField(primary_key=True,db_column='e_id')
	type = models.CharField(max_length=100)
	address =  models.CharField(max_length=200)
	contact_no =  models.CharField(max_length=20)
	google_map_link = models.CharField(max_length=1000)
	class Meta:
		db_table = 'EMERGENCY_CONTACTS'

class Roles(models.Model):
	role_id = models.AutoField(primary_key=True)
	role_name = models.CharField(max_length=20)
	def __str__(self) -> str:
		return self.role_name
	class Meta:
		db_table = 'roles'


class staff_master(models.Model):
	STAFF_ID = models.AutoField(primary_key=True)
	STAFF_NAME = models.CharField(max_length=255)
	GENDER = models.CharField(max_length=1)
	DOB = models.DateField()
	MOBILE_NO = models.CharField(max_length=20)
	EMAIL_ID = models.CharField(max_length=20,db_column="EMAIL_ID")
	JOINING_DATE = models.DateField()
	LEAVING_DATE = models.DateField()
	ACTIVE_STATUS = models.CharField(max_length=1,default='A')
	EMPLOYEE_ID = models.CharField(max_length=20)
	PASSWORD = models.CharField(max_length=20,db_column="PASSWORD")
	STAFF_ROLE = models.ForeignKey('Roles', on_delete=models.CASCADE)

	def __str__(self) -> str:
		return self.STAFF_NAME
	class Meta:
		db_table = "staff_master"

class visitor_ledger(models.Model):
	VISITOR_ID = models.AutoField(primary_key=True)  
	DATE_TIME = models.DateTimeField(auto_now_add=True)
	VISITOR_NAME = models.CharField(max_length = 100)
	PURPOSE_OF_VISIT = models.CharField(max_length = 100)
	ENTRY_DATE_TIME = models.DateTimeField()
	EXIT_DATE_TIME = models.DateTimeField()
	VISITOR_CONTACT = models.CharField(max_length = 20)
	RECORDED_BY = models.ForeignKey('staff_master',on_delete=models.CASCADE)

	class Meta:
		db_table = 'visitor_ledger'
		

class incident_types(models.Model):
	INC_TYPE_ID = models.AutoField(primary_key=True) 
	INCIDENT_TYPE = models.CharField(max_length = 50)
	def __str__(self):
		return self.INCIDENT_TYPE
	class Meta:
		db_table = 'incident_types'
	

class incidents(models.Model):
	INCIDENT  = models.AutoField(primary_key=True,db_column="INCIDENT_ID")  
	INCIDENT_TYPE = models.ForeignKey('incident_types',on_delete=models.CASCADE)
	INCIDENT_DESC = models.CharField(max_length = 500) 
	REPORTED_STAFF =  models.ForeignKey('staff_master',on_delete=models.CASCADE)
	REPORTED_DATE_TIME = models.DateTimeField() 
	ACTION = models.CharField(max_length = 500)
	STATUS = models.CharField(max_length = 1)

	class Meta:
		db_table = 'incidents'

class staff_master_view(models.Model):
	STAFF_ID = models.AutoField(primary_key=True)
	STAFF_NAME = models.CharField(max_length=255)
	GENDER = models.CharField(max_length=1)
	DOB = models.DateField()
	MOBILE_NO = models.CharField(max_length=20)
	EMAIL_ID = models.CharField(max_length=20,db_column="EMAIL_ID")
	JOINING_DATE = models.DateField()
	LEAVING_DATE = models.DateField()
	ACTIVE_STATUS = models.CharField(max_length=1,default='A')
	EMPLOYEE_ID = models.CharField(max_length=20)
	PASSWORD = models.CharField(max_length=20,db_column="PASSWORD")
	STAFF_ROLE_ID = models.IntegerField()
	ROLE_NAME = models.CharField(max_length=255)
	class Meta:
		managed = False 
		db_table = "staff_master_view"