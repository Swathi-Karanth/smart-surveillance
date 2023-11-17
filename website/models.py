from pyexpat import model
from unittest.mock import DEFAULT
from django.db import models
from django.db.models import JSONField

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
    USERNAME = models.CharField(max_length=100,default = str(STAFF_ID))
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
    INCIDENT_ID  = models.AutoField(primary_key=True,db_column="INCIDENT_ID")  
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
    USERNAME = models.CharField(max_length=100,default = str(STAFF_ID))
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

class cctv(models.Model):
    CCTV_ID =models.AutoField(primary_key=True)
    CCTV_LOCATION = models.CharField(max_length=50)
    MODEL = models.CharField(max_length=50)
    FOLDER = models.CharField(max_length=50)
    class Meta:
        db_table = 'cctv'

# class footage(models.Model):
#     FOOTAGE_ID = models.AutoField(primary_key=True)
#     START_TIMESTAMP = models.TimeField()
#     END_TIMESTAMP = models.TimeField()
#     video_folder = models.CharField(max_length=50)
#     CCTV_ID =models.ForeignKey('CCTV',on_delete=models.CASCADE)
#     class Meta:
#         db_table = 'footage'

class footage_view(models.Model):
    FOOTAGE_ID = models.AutoField(primary_key=True)
    recorded_date = models.DateTimeField()
    video_folder = models.CharField(max_length=50)
    video = models.BinaryField()
    CCTV =models.ForeignKey('CCTV',on_delete=models.CASCADE)
    cctv_location = models.CharField(max_length = 50)
    class Meta:
        db_table = 'footage_view'

    

class shift_master(models.Model):
    SHIFT_ID = models.AutoField(primary_key=True) 
    SHIFT_NAME = models.CharField(max_length=255) 
    START_TIME = models.CharField(max_length=50) 
    END_TIME = models.CharField(max_length= 50) 
    class Meta:
        db_table = 'SHIFT_MASTER'

class duty_roster(models.Model):
    STAFF_SHIFT = models.AutoField(primary_key=True,db_column='STAFF_SHIFT_ID') 
    STAFF = models.ForeignKey('staff_master',on_delete=models.CASCADE, db_column='STAFF_ID')
    SHIFT = models.ForeignKey('shift_master',on_delete=models.CASCADE, db_column='SHIFT_ID')
    START_DATE_TIME = models.DateTimeField()
    END_DATE_TIME =  models.DateTimeField()
    class Meta:
        db_table = 'DUTY_ROSTER'

class audit_change_history(models.Model):
    audit_id = models.AutoField(primary_key=True)
    parent_table_pk = models.BigIntegerField() 
    old_row_data = JSONField(null=True, blank=True) 
    new_row_data = JSONField(null=True, blank=True)
    dml_type = models.CharField(max_length=10)
    dml_timestamp = models.DateTimeField()
    audit_table_name = models.CharField(max_length=255)
    class Meta:
        db_table = 'audit_change_history'
