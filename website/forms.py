from dataclasses import fields
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# from website.views import roles


from .models import EMERGENCY_CONTACTS, incidents, staff_master,Roles,visitor_ledger

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	




# Create Add Record Form
class AddRecordForm(forms.ModelForm):
	type = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"type", "class":"form-control"}), label="type")
	address = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"address", "class":"form-control"}), label="address")
	contact_no = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"contact_no", "class":"form-control"}), label="contact_no")
	google_map_link = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"google_map_link", "class":"form-control"}), label="google_map_link")
	
	class Meta:
		model = EMERGENCY_CONTACTS
		fields = ("type","address","contact_no","google_map_link")

class AddRecordForm_staff(forms.ModelForm):
	STAFF_NAME = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Name", "class":"form-control"}), label="Staff Name")

	GENDER = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={ "class":"form-control"}), label="Gender")

	DOB = forms.DateField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"yyyy-mm-dd", "class":"form-control"}),label="DOB")
	MOBILE_NO = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={ "class":"form-control"}), label="Mobile No")

	EMAIL_ID = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"abc@gmail.com", "class":"form-control"}), label="Email ID")

	JOINING_DATE = forms.DateField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"yyyy-mm-dd", "class":"form-control"}),label="Joining Date")

	LEAVING_DATE =forms.DateField(required=False,widget=forms.widgets.TextInput(attrs={"placeholder":"yyyy-mm-dd", "class":"form-control"}),label="Leaving Date")

	ACTIVE_STATUS = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"A/N", "class":"form-control"}), label="Active Status")

	EMPLOYEE_ID = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Employee ID", "class":"form-control"}), label="Employee ID")

	PASSWORD = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Password", "class":"form-control"}), label="Password")
	
	# STAFF_ROLE_ID = forms.IntegerField(required=True, widget=forms.widgets.TextInput(attrs={"class":"form-control"}), label="Role ID")
	
	class Meta:
		model = staff_master
		fields = ("STAFF_NAME","GENDER","DOB","MOBILE_NO","EMAIL_ID","JOINING_DATE","LEAVING_DATE","ACTIVE_STATUS","EMPLOYEE_ID","PASSWORD","STAFF_ROLE")

class AddRecordForm_role(forms.ModelForm):
	# role_id = forms.IntegerField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"type", "class":"form-control"}), label="Role ID")
	role_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"type", "class":"form-control"}), label="Role Name")
	class Meta:
		model = Roles
		fields = ("role_name",)

class LoginForm(forms.ModelForm):
	username = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"username", "class":"form-control"}), label="Username")
	password = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Password", "class":"form-control"}), label="Password")


class addrecord_visitor(forms.ModelForm):
	VISITOR_NAME = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"class":"form-control"}), label="Visitor Name")
	PURPOSE_OF_VISIT = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"class":"form-control"}), label="Purpose of Visit")
	ENTRY_DATE_TIME = forms.DateTimeField(required=True, widget=forms.widgets.TextInput(attrs={"class":"form-control"}),label="Entry Date-Time")
	EXIT_DATE_TIME =forms.DateTimeField(required=True, widget=forms.widgets.TextInput(attrs={"class":"form-control"}),label="Exit Date-Time")

	VISITOR_CONTACT = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"class":"form-control"}), label="Visitor Contact")

	# RECORDED_BY_ID = models.ForeignKey(staff_master,on_delete=models.CASCADE)
	class Meta:
		model = visitor_ledger
		fields = ("VISITOR_NAME","PURPOSE_OF_VISIT","ENTRY_DATE_TIME","EXIT_DATE_TIME","VISITOR_CONTACT","RECORDED_BY")

class addincidents_form(forms.ModelForm):
	# INCIDENT_TYPE = forms.IntegerField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"type", "class":"form-control"}), label="INCIDENT TYPE ID")
	INCIDENT_DESC = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"class":"form-control"}), label="Description")

	# REPORTED_STAFF =  forms.IntegerField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"type", "class":"form-control"}), label="REPORTED STAFF ID")

	REPORTED_DATE_TIME = forms.DateTimeField(required=True, widget=forms.widgets.TextInput(attrs={"class":"form-control"}),label="Reported Date-Time")

	ACTION =forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"class":"form-control"}), label="Action")

	STATUS =forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"class":"form-control"}), label="Status")
	class Meta:
		model = incidents
		fields = ("INCIDENT_TYPE","INCIDENT_DESC","REPORTED_DATE_TIME","ACTION","STATUS","REPORTED_STAFF")

