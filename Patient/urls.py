from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('Patientclick', views.Patientclick_view,name='Patientclick'),
    path('Patientsignup', views.Patient_signup_view,name='Patientsignup'),
    path('Patient-dashboard', views.Patient_dashboard_view,name='Patient-dashboard'),
    path('Patientlogin', LoginView.as_view(template_name='insurance/adminlogin.html'),name='Patientlogin'),

    path('apply-policy', views.apply_policy_view,name='apply-policy'),
    path('apply/<int:pk>', views.apply_view,name='apply'),
    path('history', views.history_view,name='history'),

    path('ask-question', views.ask_question_view,name='ask-question'),
    path('question-history', views.question_history_view,name='question-history'),
]