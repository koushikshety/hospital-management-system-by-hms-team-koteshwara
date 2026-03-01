from django.db import models
from django import forms
from django.db import models
from django import forms

# Create your models here.
class Patient(models.Model):
    p_add = models.CharField(max_length=100)
    p_id = models.CharField(max_length=100)
    patient_name = models.CharField(max_length=100)
    date_of_birth = models.CharField(max_length=100,blank=True, null=True)
    age = models.IntegerField()
    phone = models.IntegerField()
    email = models.EmailField(max_length=100)
    gender = models.CharField(max_length=50)
    address = models.TextField()
    status = models.CharField(max_length=100)
    date = models.CharField(max_length=100,default='')
    def __str__(self):
        return self.patient_name

    def snippet(self):
        return self.email[:5]+'...'

    def snippet1(self):
        return self.address[:5]+'...'

class Doctor(models.Model):
    d_add = models.CharField(max_length=100)
    d_id = models.CharField(max_length=100)
    doctor_Name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience= models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.IntegerField()
    email = models.EmailField(max_length=100)
    gender = models.CharField(max_length=50)
    doctor_details = models.TextField()
    status = models.CharField(max_length=100)

    @property
    def d_name(self):
        return self.doctor_Name

    def __str__(self):
        return self.doctor_Name

# class doctorManager(models, Manager):
#     def doctor_Name(self):
#         return self.

class Appoint(models.Model):
    a_add = models.CharField(max_length=100)
    a_id = models.CharField(max_length=100)
    p_name =  models.CharField(max_length=100)
    pa_id = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    d_name = models.CharField(max_length=100)
    appointment_date = models.CharField(max_length=100)
    time_slot = models.CharField(max_length=100)
    token_number = models.CharField(max_length=100)
    problem = models.TextField()
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.p_name


class Payment(models.Model):
    py_add = models.CharField(max_length=100)
    py_id = models.CharField(max_length=100,default='')
    pp_id = models.CharField(max_length=100)
    patient_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)
    admission_date = models.CharField(max_length=100)
    discharge_date = models.CharField(max_length=100)
    service_name = models.CharField(max_length=100)
    cost_of_treatment = models.CharField(max_length=100)
    discount = models.CharField(max_length=100)    
    Payment_type = models.CharField(max_length=100)
    phone = models.IntegerField(blank=True, null=True)
    service_cost = models.CharField(max_length=100)
    card_no = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    card = models.CharField(max_length=100,default='')

    def __str__(self):
        return self.patient_name

    @property
    def total(self):
        return ( float(self.cost_of_treatment) + float(self.service_cost) ) - ( float(self.cost_of_treatment) + float(self.service_cost) )*(float(self.discount)/100)


class Room(models.Model):
    r_add = models.CharField(max_length=100)
    room_number = models.CharField(max_length=100)
    room_type =  models.CharField(max_length=100)
    patient_name = models.CharField(max_length=100)
    allotment_date = models.CharField(max_length=100)
    discharge_date = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.patient_name

class Blooddonner(models.Model):
    b_add = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    date_of_birth =  models.CharField(max_length=100)
    blood_group = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.EmailField(max_length=100)
    last_donation = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Dform(models.Model):
    first_name = models.CharField(max_length=100, default=None)
    last_name = models.CharField(max_length=100, default=None)
    age = models.CharField(max_length=100, default=None)
    gender = models.CharField(max_length=100, default=None)
    phone = models.CharField(max_length=100, default=None)
    email = models.EmailField(max_length=100, default=None)
    qualifications = models.CharField(max_length=100, default=None)
    file = models.FileField(max_length=100, default=None)
    address = models.TextField(null=False, default='')  # Set null=False and provide a default value or handle the empty case

    def __str__(self):
        return self.first_name + self.last_name

class Application(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    qualifications = models.TextField()
    experience = models.TextField()
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contract(models.Model):
    company_boss_name = models.CharField(max_length=100)
    boss_photo = models.ImageField(upload_to='boss_photos/',blank=True)
    company_name = models.CharField(max_length=100)
    company_address = models.CharField(max_length=200)
    services_offered = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    contract_amount = models.DecimalField(max_digits=10, decimal_places=2)
    contract_period = models.CharField(max_length=100)
    our_profit = models.DecimalField(max_digits=10, decimal_places=2)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=15)

    def __str__(self):
        return self.company_name 