from pickle import GET, NONE
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import AddRecordForm_staff, LoginForm, SignUpForm, AddRecordForm,AddRecordForm_role,addrecord_visitor
from .models import EMERGENCY_CONTACTS, Record, staff_master,visitor_ledger,incidents,staff_master_view,duty_roster,shift_master
from .models import Roles
from .forms import AddRecordForm,LoginForm,addincidents_form
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.db.models import Subquery
from django.db.models import Q



links = [
    {'ec': 'e_contact', 'title': 'Emergency Contacts','url': '/e_contact/'},
    {'r': 'roles_list','title': 'Roles', 'url': '/roles_list/'},
    {'s': 'staff','title': 'Staff', 'url': '/staff/'},
    {'v': 'visitor','title': 'Visitor Log', 'url': '/visitor_ledger/'},
    {'i': 'incident','title': 'Incident History', 'url': '/incidents/'},
    {'c': 'cctv','title': 'CCTV Footages', 'url': '/cctv_page/'},
    {'p': 'error_404','title': 'ERROR 404: Page Not Found', 'url': '/error_404/'},

    # Add more links as needed
]

def error_404(request):
    return render(request,'error_404.html',{})

def login_user(request):
    if request.user.is_authenticated == False:
    
        if request.method =="POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,username = username,password = password)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged In Successfully")
                return redirect('home')
            else:
                messages.success(request,"Error logging in, Try Again. If problem persists, contact admin.")
                return redirect('login')
                
        else:
            return render(request,'login.html',{})
    else:
            # return render(request,'home.html',{})
            return redirect('home')


def home(request):
    if request.user.is_authenticated == True:
        return render(request, 'home.html', {'links': request.role_links})
    else:
        return redirect('login')



def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    print(request.user, request.user.is_staff)	
    return redirect('login')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})

    return render(request, 'register.html', {'form':form})


def e_contact(request):
    # records = EMERGENCY_CONTACTS.objects.all()
    # print(records)
    # return render(request,'e_contact.html',{'records':records})
    if request.user.is_authenticated:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM EMERGENCY_CONTACTS")
            r = cursor.fetchall()
            records = []
            for record in r:
                data= {}
                data["e_id"] = record[0]
                data["type"] = record[1]
                data["address"] = record[2]
                data["contact_no"] = record[3]
                data["google_map_link"] = record[4]
                records.append(data)
                # print(records)
            if request.method == "GET":
                st = request.GET.get('type')
                st1 = request.GET.get('Clear')
                print(st)
                if st1 == 'Clear':
                    st = None
                    return render(request,'e_contact.html',{'records':records,'links': request.role_links})
                    
                if st is not None:
                    e = EMERGENCY_CONTACTS.objects.filter(type__icontains = st)
                    print(e)
                    data = {
                            'stdata' : e
                        }
                    return render(request,'e_contact.html',{'records':e,'links': request.role_links})
            elif st1 == 'Clear':
                # st = None
                # return render(request,'staff.html',{'records':records})
                return redirect('e_contact.html')
        return render(request,'e_contact.html',{'records':records, 'links': request.role_links})

    else:
        messages.success(request, "Warning! Unauthorized Access")
        return redirect('error_404')
    

def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look Up Records
        customer_record = EMERGENCY_CONTACTS.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated and request.user.is_staff == 1:
        delete_it = EMERGENCY_CONTACTS.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect('home')
    else:
        messages.success(request, "You Must Be Logged In as admin To Do That...")
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated and request.user.is_staff == 1:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
        return render(request, 'add_record.html', {'form':form,'links': request.role_links})
    else:
        messages.success(request, "You Must Be Logged In as Admin...")
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form, 'links': request.role_links})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')

def roles_list(request):

    if request.user.is_authenticated and request.user.is_staff == 1:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM roles")
            r = cursor.fetchall()
            records = []
            for record in r:
                data= {}
                data["role_id"] = record[0]
                data["role_name"] = record[1]
                records.append(data)
            return render(request,'roles.html',{'records':records , 'links': request.role_links})
    else:
        messages.success(request, "Warning! Unauthorized Access")
        return render(request,'error_404.html', {})
    

def add_contacts(request):
    if request.user.is_authenticated and request.user.is_staff == 1:
        return render(request,'add_contacts.html',{'form':AddRecordForm, 'links': request.role_links})
    else:
        messages.success(request, "Warning! Unauthorized Access")
        return render(request,'error_404.html', {})

def update_contacts(request,pk):
    if request.user.is_authenticated and request.user.is_staff == 1:
        if request.method=='GET':
            record = EMERGENCY_CONTACTS.objects.get(e_id=pk)
            form = AddRecordForm(request.POST or None,instance=record)
            return render(request,'update_contacts.html',{'form':form,'pk':pk, 'links': request.role_links})
        else:
            record = EMERGENCY_CONTACTS.objects.get(e_id=pk)
            form = AddRecordForm(request.POST,instance=record)
            if form.is_valid():
                form.save()
                return redirect('e_contact')
    else:
        messages.success(request, "Warning! Unauthorized Access")
        return render(request,'error_404.html', {})

def staff(request):
    if request.user.is_authenticated and request.user.is_staff == 1:
        records = staff_master_view.objects.all()
        print(records)
        if request.method == "GET":
            st = request.GET.get('STAFF_NAME')
            st1 = request.GET.get('Clear')
            print(st)
            if st1 == 'Clear':
                st = None
                return render(request,'staff.html',{'records':records,'links': request.role_links})
                
            if st is not None:
                
                staffdata = staff_master_view.objects.filter(Q(STAFF_NAME__icontains=st) | Q(EMPLOYEE_ID__in=Subquery(staff_master_view.objects.values('EMPLOYEE_ID').filter(STAFF_NAME__icontains=st))))
                # the subquery is useful because it allows you to filter the staffdata queryset by both the STAFF_NAME 
                # and EMPLOYEE_ID columns. This is useful because it allows you to find all records
                #  where the STAFF_NAME column contains the search term, even if the search term is only a partial match.
                print(staffdata)
                data = {
                        'stdata' : staffdata
                    }
                return render(request,'staff.html',{'records':staffdata,'links': request.role_links})
            elif st1 == 'Clear':
                # st = None
                # return render(request,'staff.html',{'records':records})
                return redirect('staff.html')
            
        return render(request,'staff.html',{'records':records,'links': request.role_links})
    else:
        messages.success(request, "Warning! Unauthorized Access")
        return render(request,'error_404.html', {})
    
def update_staff(request, pk):
    if request.user.is_authenticated and request.user.is_staff == 1:
        if request.method == 'GET':
            record = staff_master.objects.get(STAFF_ID=pk)
            form = AddRecordForm_staff(request.POST or None, instance=record)
            return render(request, 'update_staff.html', {'form': form, 'pk': pk, 'links': request.role_links})
        else:
            record = staff_master.objects.get(STAFF_ID=pk)
            form = AddRecordForm_staff(request.POST, instance=record)
            if form.is_valid():
                form.save()
                return redirect('staff')
    else:
        messages.success(request, "Warning! Unauthorized Access")
        return redirect('error_404')

def add_staff(request):
    form = AddRecordForm_staff(request.POST or None)
    if request.user.is_authenticated and request.user.is_staff == 1:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                record = staff_master.objects.get(pk=add_record.pk)  # You might need to adjust the condition
                column1_value = record.STAFF_NAME
                column2_value = record.PASSWORD
                column3_value = record.STAFF_ROLE
                user = User.objects.create_user(username=column1_value, password=column2_value)
                user.save()
                return redirect('home')
        return render(request, 'add_record.html', {'form':form, 'links': request.role_links})
    else:
        messages.success(request, "You Must Be Logged In as admin...")
        return redirect('home')


def add_role(request):
    form = AddRecordForm_role(request.POST or None)
    if request.user.is_authenticated and request.user.is_staff == 1:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
        return render(request, 'add_role.html', {'form':form, 'links': request.role_links})
    else:
        messages.success(request, "You Must Be Logged In as admin...")
        return redirect('home')

def visitor(request):
    if request.user.is_authenticated:
        records = visitor_ledger.objects.all()
        if request.method == "GET":
            st = request.GET.get('VISITOR_NAME')
            st1 = request.GET.get('Clear')
            if st1 == 'Clear':
                    st = None
                    return render(request,'visitor_ledger.html',{'records':records,'links': request.role_links})
            if st is not None:
                vdata = visitor_ledger.objects.filter(VISITOR_NAME__icontains = st)
                data = {
                        'stdata' : vdata
                    }
                return render(request,'visitor_ledger.html',{'records':vdata,'links': request.role_links})
            elif st1 == 'Clear':
                # st = None
                # return render(request,'staff.html',{'records':records})
                return redirect('visitor_ledger.html')
            return render(request,'visitor_ledger.html',{'records':records, 'links': request.role_links})
        else:
            messages.success(request,"You Must Be Logged In...")
            return redirect('login')


def add_visitor(request):
    form = addrecord_visitor(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
        return render(request, 'add_visitor.html', {'form':form, 'links': request.role_links})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')

def incident(request):
    if request.user.is_authenticated:
        records = incidents.objects.all()
        print(records)
        return render(request,'incidents.html',{'records':records,'links': request.role_links})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('login')

def add_incidents(request):
    form = addincidents_form(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
        return render(request, 'add_incidents.html', {'form':form, 'links': request.role_links})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')

def update_incidents(request, pk):
    if request.method=='GET':
        record = staff_master.objects.get(INCIDENT_ID=pk)
        form = AddRecordForm_staff(request.POST or None,instance=record)
        return render(request,'update_incidents.html',{'form':form,'pk':pk, 'links': request.role_links})
    else:
        record = staff_master.objects.get(INCIDENT_ID=pk)
        form = AddRecordForm_staff(request.POST,instance=record)
        if form.is_valid():
            form.save()
            return redirect('staff')
    
def delete_staff(request, pk):
    if request.user.is_authenticated and request.user.is_staff == 1:
        delete_it = staff_master.objects.get(STAFF_ID=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect('home')
    else:
        messages.success(request, "You Must Be Logged In as admin To Do That...")
        return redirect('home')

def delete_visitor(request, pk):
    if request.user.is_authenticated and request.user.is_staff == 1:
        delete_it = visitor_ledger.objects.get(VISITOR_ID=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect('home')
    else:
        messages.success(request, "You Must Be Logged In as admin To Do That...")
        return redirect('home')

def cctv_page(request):
    if request.user.is_authenticated and request.user.is_staff == 1:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM footage_view")
            r = cursor.fetchall()
            records = []
            for record in r:
                data= {}
                data["FOOTAGE_ID"] = record[0]
                data["START_TIMESTAMP"] = record[1]
                data["END_TIMESTAMP"] = record[2]
                data["FOLDER"] = record[3]
                data["CCTV_ID"] = record[4]
                data["FOLDER"] = record[5]
                records.append(data)
                # print(records)
        return render(request,'cctv.html',{'records':records,'links': request.role_links})
    else:
        messages.success(request, "Warning! Unauthorized Access")
        return redirect('error_404')

def play_video(request):
    if request.user.is_authenticated and request.user.is_staff == 1:
        return render(request, 'play_video.html', {'links': request.role_links})
    else:
        messages.success(request, "Warning! Unauthorized Access")
        return redirect('error_404')

def update_visitor(request, pk):
    if request.method=='GET':
        record = visitor_ledger.objects.get(VISITOR_ID=pk)
        form = addrecord_visitor(request.POST or None,instance=record)
        return render(request,'update_visitor.html',{'form':form,'pk':pk, 'links': request.role_links})
    else:
        record = visitor_ledger.objects.get(VISITOR_ID=pk)
        form = addrecord_visitor(request.POST,instance=record)
        if form.is_valid():
            form.save()
            return redirect('visitor_ledger')


def profile(request,pk):
    if request.user.is_authenticated:
        records = staff_master.objects.get(STAFF_NAME = pk)
        print(records.STAFF_NAME)  
        return render(request,'profile.html',{'records':records,'links': request.role_links})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('login')

def call_mysql_procedure(request):
    if request.method == 'POST':
        param1 = request.POST.get('join_from_date')
        param2 = request.POST.get('join_to_date')
        param3 = request.POST.get('age_condition')
        param4 = request.POST.get('age_range_from')
        param5 = request.POST.get('age_range_to')
        
        param1 = None if param1.lower() == 'null' else param1
        param2 = None if param2.lower() == 'null' else param2
        param3 = None if param2.lower() == 'null' else param3
        param4 = None if param4.lower() == 'null' else param4
        param5 = None if param5.lower() == 'null' else param5

        with connection.cursor() as cursor:
            cursor.callproc('staff_data_analysis', [param1, param2,param3,param4,param5,])
            # If your stored procedure returns results, fetch them
            result_set = cursor.fetchall()
            print(result_set)
        # Process the result_set if needed

    return render(request, 'procedure.html',{'links': request.role_links})

def duty(request):
    records = duty_roster.objects.all()
    return render(request,'duty.html',{'records':records,'links': request.role_links})

def shift(request):
    records = shift_master.objects.all()
    return render(request,'shift.html',{'records':records,'links': request.role_links})
    



