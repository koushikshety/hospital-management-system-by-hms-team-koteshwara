from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.db import models
from app.models import *
from app.decorators import *
from app.models import Patient,Appoint
from app.models import Doctor
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django import forms
# from .models import Application





# authentication section(sinup)
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

# authentication section(sinup,login)

def signup_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request,"Singup is Successfull..")
            login(request, user)
            messages.success(request,'Dear user, You are now succesfully Loged In')
            return redirect("index")

    else:
        form = RegistrationForm()

    return render(request, "registration/sign_up.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request,'Dear user, You are now succesfully Loged Out')
    return redirect('/')


# Basic fuction section

def index(request):
    return render(request, "index.html")

@login_required(login_url='accounts/sign_up')
def main(request):
    a = Appoint.objects.all().order_by('-appointment_date')
    user_count = User.objects.count()
    pa_count = Patient.objects.count()
    doc_count = Doctor.objects.count()
    Appoint_count = Appoint.objects.count()  # Assuming Appoint model exists
    py_count = Payment.objects.count()  # Assuming Payment model exists
    room_count = Room.objects.count()  # Assuming Room model exists

    # Get available doctors (doctor_Name and specialization)
    available_doctors = [
        {"doctor_Name": doctor.doctor_Name, "specialization": doctor.specialization}
        for doctor in Doctor.objects.filter(status="Available")
    ]

    context = {
        'user_count': user_count,
        'pa_count': pa_count,
        'doc_count': doc_count,
        'Appoint_count': Appoint_count,
        'py_count': py_count,
        'room_count': room_count,
        'available_doctors': available_doctors,
        'a':a,
    }

    return render(request, 'main.html', context)

def BASE(request):
    return render(request, 'base.html')


def ABOUT(request):
    return render(request, 'about.html')

def profile(request):
    return render(request, 'profile.html')

def TERMS(request):
    return render(request,'terms.html')





# oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooook

# ALL ID GENRATERS

def generate_patient_id():
    """Generates a new unique patient ID starting with 'P' and a two-digit number."""
    last_patient = Patient.objects.order_by('-p_id').first()
    if last_patient:
        last_id = int(last_patient.p_id[1:])
        new_id = last_id + 1
    else:
        new_id = 1
    return f"P{new_id:02}"

def generate_doctor_id():
    """Generates a new unique patient ID starting with 'P' and a two-digit number."""
    last_doctor = Doctor.objects.order_by('-d_id').first()
    if last_doctor:
        last_id = int(last_doctor.d_id[1:])
        new_id = last_id + 1
    else:
        new_id = 1
    return f"D{new_id:02}"

def generate_appoint_id():
    """Generates a new unique patient ID starting with 'P' and a two-digit number."""
    last_appoint = Appoint.objects.order_by('-a_id').first()
    if last_appoint:
        last_id = int(last_appoint.a_id[1:])
        new_id = last_id + 1
    else:
        new_id = 1
    return f"A{new_id:02}"

# def generate_payment_id():
#     """Generates a new unique patient ID starting with 'P' and a two-digit number."""
#     last_payment = Payment.objects.order_by('-py_id').first()
#     if last_payment:
#         last_id = int(last_payment.py_id[1:])
#         new_id = last_id + 1
#     else:
#         new_id = 1
#     return f"{new_id:02}"

def generate_payment_id():
    last_payment = Payment.objects.last()  # Get the last payment record
    if last_payment:
        # Extract the numeric part of the py_id (assuming format like 'Y02')
        numeric_part = last_payment.py_id[1:]  # Remove the first character (e.g., 'Y')
        try:
            last_id = int(numeric_part)  # Convert the numeric part to an integer
        except ValueError:
            # Handle the case where the numeric part is not a valid integer
            last_id = 0  # Default to 0 or handle the error as needed
    else:
        last_id = 0  # If no payments exist, start from 0

    # Increment the last ID and format it back into the desired format
    new_id = f"Y{last_id + 1:02d}"  # Format as 'Y01', 'Y02', etc.
    return new_id



#000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000


def ADD_PATIENT(request):
    if request.method == "POST":
        p_add= request.POST.get('p_add')
        
        patient_name = request.POST.get('patient_name')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        status = request.POST.get('status')
        address = request.POST.get('address')
        date = request.POST.get('date')

        # Generate a new unique patient ID
        p_id = generate_patient_id()

        patient = Patient(
            p_add=p_add,
            p_id=p_id,
            patient_name=patient_name,
            date_of_birth=dob,
            age=age,
            phone=phone,
            gender=gender,
            email=email,
            address=address,
            status=status,
            date = date,
        )
        patient.save()
        messages.success(request, "New Patient Added Successfully..")
        return redirect('add_patient')  # Redirect to the same page after adding

    return render(request, 'patients/add_patient.html')




@allowed_users(allowed_roles=['admins', 'doctors'])
def ADD_DOCTOR(request):
    if request.method == "POST":
        d_add = request.POST.get('d_add')
        doctor_name = request.POST.get('doctor_name')
        
        specialization = request.POST.get('specialization')
        experience = request.POST.get('experience')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        doctor_details = request.POST.get('doctor_details')
        gender = request.POST.get('gender')
        
        status = request.POST.get('status')
        d_id = generate_doctor_id()

        doctor = Doctor(
            d_id = d_id,
            d_add = d_add,
            doctor_Name = doctor_name,
            
            specialization =specialization,
            experience =experience,
            age = age, 
            phone = phone,
            gender = gender,
            email = email,
            
            doctor_details=doctor_details,
            status = status,
            
        )
        doctor.save()
        messages.success(request,"New Doctor Added Successfull..")

    return render(request,'Doctors/add_doctor.html')




def add_appoint(request):
    x = Doctor.objects.values_list('doctor_Name', flat=True)
    y = Patient.objects.values_list('patient_name', flat=True)
    if request.method == "POST":
        a_add= request.POST.get('a_add')
        a_id = generate_appoint_id()
        p_name =  request.POST.get('p_name')
        pa_id = request.POST.get('pa_id')
        department =request.POST.get('department')
        d_name = request.POST.get('d_name')
        appointment_date = request.POST.get('appointment_date')
        time_slot = request.POST.get('time_slot')
        token_number = request.POST.get('token_number')
        status = request.POST.get('status')
        problem = request.POST.get('problem')

        appoint = Appoint(
            a_add=a_add,
            a_id=a_id,
            p_name=p_name,
            pa_id=pa_id, 
            department=department,
            d_name=d_name,
            appointment_date=appointment_date,
            time_slot=time_slot,
            token_number=token_number,
            problem=problem,
            status=status,
        )
        appoint.save()
        messages.success(request, "New Appointment Added Successfully..")

    return render(  request, 'Appointments/add_appointment.html',  {'x': x, 'y': y} )    # , {'y':y}




@allowed_users(allowed_roles=['admins','doctors'])
def add_payment(request):
    if request.method == "POST":
        py_add = request.POST.get('py_add')
        py_id = generate_payment_id()
        pp_id = request.POST.get('pp_id')
        patient_name =  request.POST.get('patient_name')
        department =request.POST.get('department')
        doctor_name = request.POST.get('doctor_name')
        admission_date = request.POST.get('admission_date')
        discharge_date = request.POST.get('discharge_date')
        service_name = request.POST.get('service_name')
        cost_of_treatment = request.POST.get('cost_of_treatment')
        discount = request.POST.get('discount')
        Payment_type = request.POST.get('Payment_type')
        card_no = request.POST.get('card_no')
        phone = request.POST.get('phone')       
        service_cost = request.POST.get('service_cost')
        status = request.POST.get('status')
        card = request.POST.get('card')

        payment = Payment(
            py_add = py_add,
            pp_id = pp_id,
            py_id = py_id,
            patient_name = patient_name,
            department = department,
            doctor_name= doctor_name,
            admission_date = admission_date,
            discharge_date = discharge_date,
            service_name = service_name,
            cost_of_treatment = cost_of_treatment,
            discount = discount,
            Payment_type=Payment_type,
            card_no=card_no,
            phone=phone,
            card = card,
            service_cost=service_cost,
            status = status,
            
        )
        payment.save()
        messages.success(request,"New Payment Added Successfull..")

    return render(request, 'Payments/add_payment.html')

@allowed_users(allowed_roles=['admins','doctors','patients'])
def add_room(request):
    y = Patient.objects.all()
    if request.method == "POST":
        r_add= request.POST.get('r_add')
        room_number = request.POST.get('room_number')
        room_type = request.POST.get('room_type')
        patient_name =  request.POST.get('patient_name')
        allotment_date = request.POST.get('allotment_date')
        discharge_date = request.POST.get('discharge_date')
        doctor_name = request.POST.get('doctor_name')
        status = request.POST.get('status')

        room = Room(
            r_add = r_add,
            room_number=room_number,
            room_type = room_type,
            patient_name=patient_name,
            allotment_date = allotment_date,
            discharge_date = discharge_date,
            doctor_name= doctor_name,           
            status = status,
            
        )
        room.save()
        messages.success(request,"New Room Added Successfull..")

    return render(request, 'Room_Allotments/add_room.html',{'y':y })



#Patient fuction section
# @allowed_users(allowed_roles=['admins','doctors','patients'])
def ALL_PATIENT(request):
    patient_details = Patient.objects.all().order_by('p_id')
    return render(request,'patients/all_patients.html',{'patient_details':patient_details})


def about(request):
    patient_detail = Patient.objects.all().order_by('p_id')
    return render(request, 'patients/Patient_details1.html', {'patient_detail': patient_detail})

@allowed_users(allowed_roles=['admins'])
def PATIENT_DETAILS(request, id):
    patient = Patient.objects.get(id=id)
    available_doctors = Appoint.objects.filter(p_name=patient.patient_name)
    pay2 = Payment.objects.filter(patient_name=patient.patient_name)
    pay = Payment.objects.filter(patient_name=patient.patient_name)
    
    context = {
        'patient': patient,
        'available_doctors': available_doctors,
        'pay': pay,
        'pay2':pay2
    }
    
    return render(request, 'patients/Patient_details.html', context)



def delete(request, id):  
    dele = Patient.objects.get(id=id)
    dele.delete()
    messages.success(request," request is Successfull, Patient is Deleted...")
    return redirect('all_patients')

def p_update(request, id):
    edit = Patient.objects.get(id=id)
    
    if request.method == "POST":
        p_id =  request.POST.get('p_id')
        patient_name = request.POST.get('patient_name')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        status = request.POST.get('status')
        address = request.POST.get('address')
        
        edit.p_id = p_id
        edit.patient_name = patient_name
        edit.dob = dob
        edit.age = age
        edit.phone = phone
        edit.email = email
        edit.gender = gender
        edit.status = status
        edit.address = address
        edit.save()
        messages.success(request, 'infomation updated sucessfully')
        return redirect('all_patients')
        
    return render(request, 'patients/p_update.html', {'edit': edit})





# Doctors fuction section


def all_doctor(request):
    doctor_detail = Doctor.objects.all().order_by('id')
    return render(request,'Doctors/all_doctors.html',{'doctor_detail':doctor_detail})


# doctor_details1 views.py start here

def about_doctor(request):
    doctor_detail = Doctor.objects.all().order_by('id')
    doctor_appointments = Appoint.objects.filter(d_name__in=[doctor.doctor_Name for doctor in doctor_detail])

    context = {
        'doctor_detail': doctor_detail,
        'doctor_appointments': doctor_appointments,
    }

    return render(request, 'Doctors/doctor_details1.html', context)

# views.py ends here

@allowed_users(allowed_roles=['admins','doctors'])
def DOCTOR_DETAILS(request, id):
    doctor_detail = Doctor.objects.get(id=id)
    appointments = Appoint.objects.filter(d_name=doctor_detail.doctor_Name)
    return render(request, 'Doctors/doctor_details.html', {'doctor_detail': doctor_detail, 'appointments': appointments})

def delete2(request, id):
    
    dele2 = Doctor.objects.get(id=id)
    dele2.delete()
    messages.success(request," request is Successfull, Doctor is Deleted...")
    return redirect('all_doctor')



def edit_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    
    if request.method == "POST":
        doctor.doctor_Name = request.POST.get('doctor_name')
        doctor.date_of_birth = request.POST.get('dob')
        doctor.specialization = request.POST.get('specialization')
        doctor.experience = request.POST.get('experience')
        doctor.age = int(request.POST.get('age'))
        doctor.phone = int(request.POST.get('phone'))
        doctor.email = request.POST.get('email')
        doctor.gender = request.POST.get('gender')
        doctor.address = request.POST.get('address')
        doctor.d_id = request.POST.get("d_id")
        doctor.status = request.POST.get('status')
        doctor.save()
        messages.success(request, 'infomation updated sucessfully')
        return redirect('all_doctor')
        
    return render(request, 'Doctors/d_update.html', {'doctor': doctor})

#Appointment section

@allowed_users(allowed_roles=['admins','doctors','patients'])
def all_appoint(request):
    appoint_detail = Appoint.objects.all().order_by('a_id')
    return render(request,'Appointments/all_appointments.html',{'appoint_detail':appoint_detail})

@allowed_users(allowed_roles=['admins','doctors'])
def about_appoint(request):
    appoint_detail = Appoint.objects.all().order_by('a_id')
    return render(request, 'Appointments/appointment_details1.html', {'appoint_detail': appoint_detail})

@allowed_users(allowed_roles=['admins','doctors'])
def APPOINT_DETAILS(request, id):
    appoint_detail = Appoint.objects.get(id=id)
    return render(request,'Appointments/appointment_details.html',{'appoint_detail':appoint_detail})


def deleteapp(request, id):
    
    dele = Appoint.objects.get(id=id)
    dele.delete()
    messages.success(request," request is Successfull, Appointment is Deleted...")
    return redirect('all_appointment')


def edit_appoint(request, id):
    x= get_object_or_404(Appoint, id=id)
    
    if request.method == "POST":
        x.a_id = request.POST.get('a_id')
        x.p_name =  request.POST.get('p_name')
        x.pa_id = request.POST.get('pa_id')
        x.department =request.POST.get('department')
        x.d_name = request.POST.get('d_name')
        x.appointment_date = request.POST.get('appointment_date')
        x.time_slot = request.POST.get('time_slot')
        x.token_number = request.POST.get('token_number')
        x.status = request.POST.get('status')
        x.problem = request.POST.get('problem')
        x.save()
        messages.success(request, 'infomation updated sucessfully')
        return redirect('all_appointment')
        
    return render(request, 'Appointments/edit_appoint.html', {'x':x })

#payments section

@allowed_users(allowed_roles=['admins','doctors','patients'])
def all_payment(request):
    payment_detail = Payment.objects.all().order_by('id')
    return render(request, 'Payments/all_payment.html', {'payment_detail': payment_detail})

# def PAY_DETAILS(request, id):
#     py = Payment.objects.get(id=id)
#     return render(request, 'Doctors/doctor_details.html', {'py': py})


def deletepay(request, id):
    dele = Payment.objects.get(id=id)
    dele.delete()
    messages.success(request," request is Successfull, Payment is Deleted...")
    return redirect('all_payment')

def edit_payment(request, id):
    x= get_object_or_404(Payment, id=id)


    if request.method == "POST":
        x.pp_id = request.POST.get('pp_id')
        x.patient_name =  request.POST.get('patient_name')
        x.department =request.POST.get('department')
        x.doctor_name = request.POST.get('doctor_name')
        x.admission_date = request.POST.get('admission_date')
        x.discharge_date = request.POST.get('discharge_date')
        x.service_name = request.POST.get('service_name')
        x.cost_of_treatment = request.POST.get('cost_of_treatment')
        x.discount = request.POST.get('discount')
        x.advance_paid = request.POST.get('advance_paid')
        x.Payment_type = request.POST.get('Payment_type')
        x.card_no = request.POST.get('card_no')
        x.status = request.POST.get('status')
        x.save()
        messages.success(request, 'infomation updated sucessfully')
        return redirect('all_payment')
        
    return render(request, 'Payments/edit_payment.html', {'x':x })


@allowed_users(allowed_roles=['admins','doctors'])
def invoice(request):
    return render(request,'Payments/invoice.html')

# @allowed_users(allowed_roles=['admins','doctors'])
def invoice2(request,id):
    payment_detail = Payment.objects.get(id=id)
    total = Payment.total

    return render(request,'Payments/invoice2.html',{ 'payment_detail': payment_detail})


# Room section 
def all_room(request):
    room_detail = Room.objects.all().order_by('room_number')
    return render(request, 'Room_Allotments/all_room.html', {'room_detail': room_detail})




def edit_room(request, id):
    x= get_object_or_404(Room, id=id)
    if request.method == "POST":
        # x.r_add= request.POST.get('r_add')
        x.room_number = request.POST.get('room_number')
        x.room_type = request.POST.get('room_type')
        x.patient_name =  request.POST.get('patient_name')
        x.allotment_date = request.POST.get('allotment_date')
        x.discharge_date = request.POST.get('discharge_date')
        x.doctor_name = request.POST.get('doctor_name')
        x.status = request.POST.get('status')
        x.save()
        messages.success(request, 'infomation updated sucessfully')
        return redirect('all_room')
        
    return render(request, 'Room_Allotments/edit_room.html', {'x':x })

def deleteroom(request, id):
    
    dele = Room.objects.get(id = id)
    dele.delete()
    messages.success(request," request is Successfull, A Room is Deleted...")
    return redirect('all_room')

#Resource_Pages
def map(request):
    return render(request, 'Resource_Pages/map.html')

def typography(request):
    return render(request, 'Resource_Pages/typography.html')

def form(request):
    return render(request, 'Resource_Pages/form.html')

#other_pages

def faq(request):
    return render(request, 'Other_Pages/faq.html')

def sub(request):
    return render(request, 'Other_Pages/price.html')

def bd(request):
    if request.method == "POST":
        b_add= request.POST.get('b_add')
        name = request.POST.get('name')
        date_of_birth = request.POST.get('date_of_birth')
        blood_group =  request.POST.get('blood_group')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        last_donation = request.POST.get('last_donation')

        bd = Blooddonner(
            b_add = b_add,
            name=name,
            date_of_birth = date_of_birth,
            blood_group=blood_group,
            phone = phone,
            email = email,
            last_donation= last_donation,           
            
        )
        bd.save()
        messages.success(request,"New BloodDonner Added Successfull..")
        return redirect('blooddonner')

    return render(request, 'Other_Pages/blooddoner.html')

def schedule(request):
    return render(request,'Other_Pages/schedule.html')


#newdoctorform views comes here

def new_doctor_application(request):
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        file = request.POST.get('file')
        address = request.POST.get('address')  # Uncomment this line
        gender = request.POST.get('gender')
        qualifications = request.POST.get('qualifications')

        dform = Dform(
            first_name=first_name,
            last_name=last_name,
            age=age,
            phone=phone,
            email=email,
            address=address,  # Add address here
            gender=gender,
            file=file,
            qualifications=qualifications,
        )
        dform.save()
        messages.success(request, "Your Doctor Application Added Successfully. Please Wait! Hospital Services Will Contact You Soon.")
    
    return render(request, 'Resource_Pages/form.html')


def new_doctor_application(request):
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        file = request.POST.get('file')
        address = request.POST.get('address')  # Uncomment this line
        gender = request.POST.get('gender')
        qualifications = request.POST.get('qualifications')

        dform = Dform(
            first_name=first_name,
            last_name=last_name,
            age=age,
            phone=phone,
            email=email,
            address=address,  # Add address here
            gender=gender,
            file=file,
            qualifications=qualifications,
        )
        dform.save()
        messages.success(request, "Your Doctor Application Added Successfully. Please Wait! Hospital Services Will Contact You Soon.")
    
    return render(request, 'Resource_Pages/form.html')


def application(request):
    if request.method == "POST":
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        qualifications = request.POST.get('qualifications')
        experience = request.POST.get('experience')
        date_of_birth = request.POST.get('date_of_birth')

        application_instance = Application(
            name=name,
            gender=gender,
            email=email,
            phone=phone,
            address=address,
            qualifications=qualifications,
            experience=experience,
            date_of_birth=date_of_birth
        )
        messages.success(request, "Your Application Added Successfully. Please Wait! Hospital Services Will Contact You Soon.")
        application_instance.save()
    else:
        messages.success(request, "Your Application Failed. Please Wait! Hospital Services Will Contact You Soon.")
        return redirect("form")
        
    return render(request, 'Resource_Pages/form.html')

def contract_form(request):
    if request.method == 'POST':
        # Retrieve form data
        company_boss_name = request.POST['companyBossName']
        # Retrieve uploaded file
        boss_photo = request.POST['bossPhoto']
        company_name = request.POST['companyName']
        company_address = request.POST['companyAddress']
        services_offered = request.POST['servicesOffered']
        start_date = request.POST['startDate']
        end_date = request.POST['endDate']
        contract_amount = request.POST['contractAmount']
        contract_period = request.POST['contractPeriod']
        our_profit = request.POST['ourProfit']
        client_name = request.POST['clientName']
        client_email = request.POST['clientEmail']
        client_phone = request.POST['clientPhone']

        # Create Contract object
        contract = Contract(
            company_boss_name=company_boss_name,
            boss_photo=boss_photo,
            company_name=company_name,
            company_address=company_address,
            services_offered=services_offered,
            start_date=start_date,
            end_date=end_date,
            contract_amount=contract_amount,
            contract_period=contract_period,
            our_profit=our_profit,
            client_name=client_name,
            client_email=client_email,
            client_phone=client_phone
        )
        # Save the contract to the database
        messages.success(request, "Your Contract Added Successfully. Please Wait! Hospital Services Will Contact You Soon.")
        contract.save()
        
    return render(request, 'Resource_Pages/form.html')