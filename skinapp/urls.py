from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
    
    path('',views.userlogin,name='userlogin'),
    path('userregister/',views.userregister,name='userregister'),
    path('prediction/',views.prediction,name='prediction'),
    path('booking/',views.booking,name='booking'),
    path('appointment/',views.appointment,name='appointment'),
    path('doctor/',views.doctorlogin,name='doctorlogin'),
    path('index/',views.index,name='index'),
     path('bookings/',views.bookings,name='bookings'),
path('delete_appointment/<int:booking_id>/',views.delete_appointment,name='delete_appointment'),

    path('dindex/',views.dindex,name='dindex'),
    # path('admin/',views.adddoctor,name='adddoctor'),
    path('doctor_registration/',views.doctorregister,name='doctorregister'),
    path('doctorlogin/',views.doctorlogin,name='doctorlogin'),
    path('viewappointment/',views.viewappointment,name='viewappoinment'),
    path('logout/',views.logout,name='logout'),

    path('dlogout/',views.dlogout,name='dlogout'),

    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('aindex/',views.aindex,name='aindex'),
    path('alogout/',views.alogout,name='alogout'),
    path('viewdoctors/',views.viewdoctors,name='viewdoctors'),
    path('viewpatient/',views.viewpatient,name='viewpatient'),
    path('adminappointment/',views.adminappointment,name='adminappointment'),
   path('add_doctor_details/',views.add_doctor_details,name='add_doctor_details'),
   path('view_requests/',views.view_requests,name='view_requests'),
   path('approve/<int:request_id>/',views.approve,name='approve'),
   path('reject/<int:request_id>/',views.reject,name='reject'),
    path('delete/<int:user_id>/',views.delete,name='delete'),
    path('schedule_consultation/',views.schedule_consultation,name='schedule_consultation'),
 path('viewschedules/',views.viewschedules,name='viewschedules'),
  path('deleteschedule/<int:schedule_id>/',views.deleteschedule,name='deleteschedule'),

]
