from datetime import datetime
from operator import le
import re
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.urls import reverse
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
from sklearn.preprocessing import LabelEncoder
from .models import Appointment, ConsultationSchedule,Doctor_details

from django.core.files.storage import FileSystemStorage

from PIL import Image
import numpy as np
import cv2
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import send_mail

# Create your views here.



def userlogin(request):
    if request.method=='POST':
        uname=request.POST.get('uname')
        password=request.POST.get('password')
        user=auth.authenticate(username=uname,password=password)
        if user is not None:
            auth.login(request,user)
            return render(request,'index.html')
        else:
            messages.info(request,"invalid entry")
    return render(request,'userlogin.html')

def userregister(request):
    if request.method=='POST':
        name=request.POST.get('name')
        uname=request.POST.get('uname')
        email=request.POST.get('email')
        password=request.POST.get('password')
        cpass=request.POST.get('cpass')

        if len(password) < 8:
            messages.info(request, "Password must be at least 8 characters long.")
        elif not re.search(r'\d', password):
            messages.info(request, "Password must contain at least one digit.")
        elif not re.search(r'[a-zA-Z]', password):
            messages.info(request, "Password must contain at least one letter.")
        elif password != cpass:
            messages.info(request, "Passwords do not match.")

        
        elif User.objects.filter(username=uname).exists():
                messages.info(request,"username already taken")
        elif User.objects.filter(email=email).exists():
                messages.info(request,"email already taken")
        else:
            user = User.objects.create_user(first_name=name, username=uname, email=email, password=password)
            user.save()
            subject="Welcome"
            message='Hey, '+uname+' , SKIN SURE welcomes you to our family..'
            to=email
            send_mail(subject,message,settings.EMAIL_HOST_USER,[to],fail_silently=False)
            return render(request,'userlogin.html')
        
    return render(request,'userregister.html')

# def prediction(request):
#     model = load_model('skin_model.h5')
#     if request.method == 'POST' and request.FILES['img']:
#         uploaded_image = request.FILES['img']
#         fs = FileSystemStorage()
#         image_path = fs.save(uploaded_image.name, uploaded_image)
#         image_url = fs.url(image_path)

#         img = image.load_img('media/' + image_path, target_size=(224, 224))
#         img_array = image.img_to_array(img)
#         img_array = np.expand_dims(img_array, axis=0)
#         img_array = preprocess_input(img_array)

#         le = LabelEncoder()
   
#         le.classes_=['BA- cellulitis', 'BA-impetigo', 'FU-athlete-foot',
#        'FU-nail-fungus', 'FU-ringworm', 'PA-cutaneous-larva-migrans',
#        'VI-chickenpox', 'VI-shingles']
#         prediction = model.predict(img_array)
#         predicted_class = np.argmax(prediction)
#         predicted_label = le.classes_[predicted_class]

#         cures={'BA- cellulitis':'Cellulitis treatment usually includes a prescription oral antibiotic. Within three days of starting an antibiotic, let your health care provider know whether the infection is responding to treatment. You will need to take the antibiotic for the full course, usually 5 to 10 days, even if you start to feel better.',
#               'BA-impetigo':'Topical antibiotics alone or in conjunction with systemic antibiotics are used to treat impetigo. Antibiotic coverage should cover both S aureus and S pyogenes (i.e. GABHS). While untreated impetigo is often self-limiting, antibiotics decrease the duration of illness and spread of lesions.',
#               'FU-athlete-foot':'Use an antifungal product.The antifungal terbinafine (Lamisil AT) has been shown to be very effective. Another option is clotrimazole (Lotrimin AF). You may need to experiment to find the product and formulation — ointment, gel, cream, lotion, powder or spray — that work for you.',
#               'FU-nail-fungus':'Try nonprescription antifungal nail creams and ointments. Several products are available, such as terbinafine (Lamisil).Trim and thin the nails. This helps reduce pain by reducing pressure on the nails.',
#               'FU-ringworm':'Ringworm on the skin like athletes foot (tinea pedis) and jock itch (tinea cruris) can usually be treated with non-prescription antifungal creams, lotions, or powders applied to the skin for 2 to 4 weeks. There are many non-prescription products available to treat ringworm, including: Clotrimazole (Lotrimin, Mycelex)',
#               'PA-cutaneous-larva-migrans':'CLM is self-limiting; migrating larvae usually die after 5–6 weeks. Albendazole is a very effective treatment. Ivermectin is effective but not approved by the US Food and Drug Administration for this indication. Symptomatic treatment can help relieve severe itching and reduce the chance of bacterial superinfection.',
#               'VI-chickenpox':'If you or your child is at high risk of complications, your provider may suggest antiviral medicine to fight the virus, such as acyclovir (Zovirax, Sitavig). This medicine may lessen the symptoms of chickenpox. But they work best when given within 24 hours after the rash first appears.',
#               'VI-shingles':'There is no cure for shingles. Early treatment with prescription antiviral drugs may speed healing and lower your risk of complications. These drugs include: Acyclovir (Zovirax)'}
#         cure=[]
#         if predicted_label:
#             cure=cures[predicted_label]
#         request.session['name'] = request.user.username 
#         request.session['disease'] = predicted_label
#         request.session['image_url'] = image_url
      
#         # Display the result
#         context = {'image_url': image_url, 'predicted_label': predicted_label,'cure':cure}
#         return render(request, 'prediction.html', context)
#     return render(request, 'index.html')


def prediction(request):
    model = load_model('skin_model.h5')
    if request.method == 'POST' and request.FILES['img']:
        uploaded_image = request.FILES['img']
        fs = FileSystemStorage()
        image_path = fs.save(uploaded_image.name, uploaded_image)
        image_url = fs.url(image_path)

        img = image.load_img('media/' + image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        le = LabelEncoder()
        le.classes_=['BA- cellulitis', 'BA-impetigo', 'FU-athlete-foot',
       'FU-nail-fungus', 'FU-ringworm', 'PA-cutaneous-larva-migrans',
       'VI-chickenpox', 'VI-shingles']
        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction)
        predicted_label = le.classes_[predicted_class]

        # Define threshold for non-disease classification
        threshold = 0.6

        cures={'BA- cellulitis':'Cellulitis treatment usually includes a prescription oral antibiotic. Within three days of starting an antibiotic, let your health care provider know whether the infection is responding to treatment. You will need to take the antibiotic for the full course, usually 5 to 10 days, even if you start to feel better.',
              'BA-impetigo':'Topical antibiotics alone or in conjunction with systemic antibiotics are used to treat impetigo. Antibiotic coverage should cover both S aureus and S pyogenes (i.e. GABHS). While untreated impetigo is often self-limiting, antibiotics decrease the duration of illness and spread of lesions.',
              'FU-athlete-foot':'Use an antifungal product.The antifungal terbinafine (Lamisil AT) has been shown to be very effective. Another option is clotrimazole (Lotrimin AF). You may need to experiment to find the product and formulation — ointment, gel, cream, lotion, powder or spray — that work for you.',
              'FU-nail-fungus':'Try nonprescription antifungal nail creams and ointments. Several products are available, such as terbinafine (Lamisil).Trim and thin the nails. This helps reduce pain by reducing pressure on the nails.',
              'FU-ringworm':'Ringworm on the skin like athletes foot (tinea pedis) and jock itch (tinea cruris) can usually be treated with non-prescription antifungal creams, lotions, or powders applied to the skin for 2 to 4 weeks. There are many non-prescription products available to treat ringworm, including: Clotrimazole (Lotrimin, Mycelex)',
              'PA-cutaneous-larva-migrans':'CLM is self-limiting; migrating larvae usually die after 5–6 weeks. Albendazole is a very effective treatment. Ivermectin is effective but not approved by the US Food and Drug Administration for this indication. Symptomatic treatment can help relieve severe itching and reduce the chance of bacterial superinfection.',
              'VI-chickenpox':'If you or your child is at high risk of complications, your provider may suggest antiviral medicine to fight the virus, such as acyclovir (Zovirax, Sitavig). This medicine may lessen the symptoms of chickenpox. But they work best when given within 24 hours after the rash first appears.',
              'VI-shingles':'There is no cure for shingles. Early treatment with prescription antiviral drugs may speed healing and lower your risk of complications. These drugs include: Acyclovir (Zovirax)'}
        
        # If prediction probability is above threshold, consider it as a disease
       
        if np.max(prediction) > threshold:
            # Check if predicted label is a valid disease label
            if predicted_label in cures:
                cure = cures[predicted_label]
            else:
                predicted_label = "Non-Disease"
                cure = "No specific treatment required for non-disease images."
        else:
            predicted_label = "Non-Disease"
            cure = "No specific treatment required for non-disease images."

        request.session['name'] = request.user.username 
        request.session['disease'] = predicted_label
        request.session['image_url'] = image_url
      
        # Display the result
        context = {'image_url': image_url, 'predicted_label': predicted_label,'cure':cure}
        return render(request, 'prediction.html', context)
    return render(request, 'index.html')


def appointment(request):
    if request.method == 'POST':
        patient = request.user 
        disease=request.POST.get('disease')
        image_url = request.POST.get('image_url')     
        doctor_username = request.POST.get('doctor')
        doctor = User.objects.get(username=doctor_username)
        appointment_date = request.POST.get('date') + ' ' + request.POST.get('time')
        
        try:
            consultation_schedule = ConsultationSchedule.objects.get(doctor__doctor=doctor, 
                                                                     day_of_week=datetime.strptime(appointment_date, '%Y-%m-%d %H:%M').weekday())
        except ConsultationSchedule.DoesNotExist:
            messages.error(request, 'Consultation schedule for the selected doctor on the chosen day does not exist.')
            return redirect('booking')

        if not consultation_schedule.start_time <= datetime.strptime(appointment_date, '%Y-%m-%d %H:%M').time() <= consultation_schedule.end_time:
            messages.error(request, 'The selected time slot is not available for this doctor. Please choose another time.')
            return redirect('booking')


        if Appointment.objects.filter(appointment_date=appointment_date).exists():
            messages.error(request, 'The selected time slot is already booked. Please choose another time.')
            return redirect('booking')
        appointment = Appointment.objects.create(patient=patient,disease=disease, doctor=doctor, appointment_date=appointment_date,image=image_url)
        appointment.save()
        subject="BOOKING"
        message='Hey, '+patient.username+' , You are booked your time with Dr.'+doctor_username+' on '+appointment_date+'.'
        to=patient.email
        send_mail(subject,message,settings.EMAIL_HOST_USER,[to],fail_silently=False)
    return render(request,'appointment.html')

def booking(request):
    name = request.session.get('name', '')
    disease = request.session.get('disease', '')
    img=request.session.get('image_url','')
    doctors = Doctor_details.objects.filter(approved=True)
    schedules=ConsultationSchedule.objects.all()
    return render(request,'booking.html',{'name':name,'disease':disease,'doctors':doctors,'image_url':img,'schedules':schedules})

#Doctor

def doctorregister(request):
    if request.method=='POST':
        drname='Dr.'
        name=drname+request.POST.get('name')
        uname=request.POST.get('uname')
        email=request.POST.get('email')
        password=request.POST.get('password')
        cpass=request.POST.get('cpass')

        if len(password) < 8:
            messages.info(request, "Password must be at least 8 characters long.")
        elif not re.search(r'\d', password):
            messages.info(request, "Password must contain at least one digit.")
        elif not re.search(r'[a-zA-Z]', password):
            messages.info(request, "Password must contain at least one letter.")
        elif password != cpass:
            messages.info(request, "Passwords do not match.")

     
        elif User.objects.filter(username=uname).exists():
                messages.info(request,"username already taken")
        elif User.objects.filter(email=email).exists():
                messages.info(request,"email already taken")
        else:
            user = User.objects.create_user(first_name=name, username=uname, email=email, password=password)
            user.save()
            subject="Welcome"
            message='Hey, '+uname+' , SKIN SURE welcomes you to our family..'
            to=email
            send_mail(subject,message,settings.EMAIL_HOST_USER,[to],fail_silently=False)
            return render(request,'doctor/adddetails.html',{'user': user})
    return render(request,'doctor/doctorregister.html')

def doctorlogin(request):
    if request.method=='POST':
        uname=request.POST['uname']
        password=request.POST['password']
        user=auth.authenticate(username=uname,password=password)
        if user is not None:
            doctor_details = Doctor_details.objects.filter(doctor=user).first()  
            if doctor_details and doctor_details.approved:
                auth.login(request,user)
                return redirect('dindex')
            else:
                messages.error(request, "Your account has not been approved yet or you are not a doctor.")
        else:
            messages.info(request,"invalid entry")
    return render(request,'doctor/doctorlogin.html')

def index(request):
    return render(request,'index.html')

def viewappointment(request): 
    doctor = request.user
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-id')
    doctor_details=Doctor_details.objects.filter(doctor=request.user).first()

    return render(request,'doctor/viewappoinments.html',{'appointments':appointments,'doctor_details':doctor_details})

def dindex(request):
    doctor_details=Doctor_details.objects.filter(doctor=request.user).first()
    return render(request,'doctor/dindex.html',{'doctor_details':doctor_details})

def logout(request):
    auth.logout(request)
    return redirect('userlogin') 

def dlogout(request):
    auth.logout(request)
    return redirect('doctorlogin') 

#Admin

def adminlogin(request):
    if request.method=='POST':
        uname=request.POST['uname']
        password=request.POST['password']
        user=auth.authenticate(username=uname,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('aindex')
        else:
            messages.info(request,"invalid entry")
    return render(request,'admin/alogin.html')

def aindex(request):
    return render(request,'admin/aindex.html')

def alogout(request):
    auth.logout(request)
    return redirect('adminlogin') 

def viewdoctors(request):
    doctors = Doctor_details.objects.filter(approved=True)
    return render(request,'admin/doctor.html',{'doctors':doctors})

def viewpatient(request):
    patients = User.objects.exclude(first_name__contains='Dr.')
    return render(request,'admin/patient.html',{'patients':patients})

def adminappointment(request):
    appointments = Appointment.objects.all()
    return render(request, 'admin/viewappoinments.html', {'appointments': appointments})

def add_doctor_details(request):

    if request.method == 'POST':
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        cv = request.FILES.get('cv')
        user_id = request.POST.get('id')
        doctor = User.objects.get(id=user_id)
        new_doctor_details = Doctor_details(
            doctor=doctor,
            qualification=qualification,
            experience=experience,
            cv=cv
        )
        new_doctor_details.save()
        return render(request,'doctor/doctorlogin.html',{'new_doctor_details':new_doctor_details})
    else:
        return render(request, 'doctor/adddetails.html') 
    
def view_requests(request):
    requests=Doctor_details.objects.filter(approved=False).order_by('-id')
    return render(request,'admin/request.html',{'requests':requests})

def approve(request, request_id):
    doctor_request = get_object_or_404(Doctor_details, id=request_id)
    doctor_request.approved = True
    doctor_request.save()
    subject="Approved"
    message='Hey, '+doctor_request.doctor.username+' , You request Approved.....Best Wishes...'
    to=doctor_request.doctor.email
    send_mail(subject,message,settings.EMAIL_HOST_USER,[to],fail_silently=False)
    return redirect('view_requests')

def reject(request, request_id):
    doctor_request = get_object_or_404(Doctor_details, id=request_id)
    doctor_request.rejected = True
    doctor_request.save()
    subject="Rejected"
    message='Hey, '+doctor_request.doctor.username+' , You request Rejected...Sorry...'
    to=doctor_request.doctor.email
    send_mail(subject,message,settings.EMAIL_HOST_USER,[to],fail_silently=False)
    return redirect('view_requests')

def delete(request,user_id):
    user=User.objects.get(id=user_id)
    user.delete()
    return redirect('viewdoctors')


def bookings(request):
    user=request.user
    bookings=Appointment.objects.filter(patient=user).order_by('-id')
    return render(request,'bookings.html',{'bookings':bookings})


def delete_appointment(request,booking_id):
    booking=Appointment.objects.filter(id=booking_id)
    booking.delete()
    return redirect('bookings')


def schedule_consultation(request):
    doctors = Doctor_details.objects.filter(approved=True)
    if request.method == 'POST':
        doctor_id = int(request.POST.get('doctor'))
        day_of_week = request.POST.get('day_of_week')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        doctor = Doctor_details.objects.get(doctor_id=doctor_id)
        consultation_schedule = ConsultationSchedule.objects.create(
                doctor=doctor,
                day_of_week=day_of_week,
                start_time=start_time,
                end_time=end_time
            )
        consultation_schedule.save()    
    return render(request, 'doctor/schedule_time.html', {'doctors': doctors})


def viewschedules(request):
    schedules=ConsultationSchedule.objects.all()
    day_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    for schedule in schedules:
        schedule.day_of_week = day_names[schedule.day_of_week]
    return render(request,'doctor/view_schedules.html',{'schedules':schedules})

def deleteschedule(request,schedule_id):
    schedule=ConsultationSchedule.objects.get(id=schedule_id)
    schedule.delete()
    return redirect('viewschedules')
