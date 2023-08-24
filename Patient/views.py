from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from insurance import models as CMODEL
from insurance import forms as CFORM
from django.contrib.auth.models import User


def Patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'customer/customerclick.html')


def customer_signup_view(request):
    userForm=forms.PatientUserForm()
    PatientForm=forms.PatientForm()
    mydict={'userForm':userForm,'PatientForm':PatientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        PatientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and PatientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            Patient=PatientForm.save(commit=False)
            Patient.user=user
            Patient.save()
            my_Patient_group = Group.objects.get_or_create(name='Patient')
            my_Patient_group[0].user_set.add(user)
        return HttpResponseRedirect('Patientlogin')
    return render(request,'/Patientsignup.html',context=mydict)

def is_Patient(user):
    return user.groups.filter(name='Patient').exists()

@login_required(login_url='Patientlogin')
def customer_dashboard_view(request):
    dict={
        'customer':models.Patient.objects.get(user_id=request.user.id),
        'available_policy':CMODEL.Policy.objects.all().count(),
        'applied_policy':CMODEL.PolicyRecord.objects.all().filter(Patient=models.Patient.objects.get(user_id=request.user.id)).count(),
        'total_category':CMODEL.Category.objects.all().count(),
        'total_question':CMODEL.Question.objects.all().filter(customer=models.Patient.objects.get(user_id=request.user.id)).count(),

    }
    return render(request,'customer/customer_dashboard.html',context=dict)

def apply_policy_view(request):
    Patient= models.Patient.objects.get(user_id=request.user.id)
    policies = CMODEL.Policy.objects.all()
    return render(request,'customer/apply_policy.html',{'policies':policies,'customer':Patient})

def apply_view(request,pk):
    customer = models.Patient.objects.get(user_id=request.user.id)
    policy = CMODEL.Policy.objects.get(id=pk)
    policyrecord = CMODEL.PolicyRecord()
    policyrecord.Policy = policy
    policyrecord.Patient = Patient
    policyrecord.save()
    return redirect('history')

def history_view(request):
    Patient = models.Patient.objects.get(user_id=request.user.id)
    policies = CMODEL.PolicyRecord.objects.all().filter(Patient=Patient)
    return render(request,'customer/history.html',{'policies':policies,'Patient':Patient})

def ask_question_view(request):
    Patient = models.Patient.objects.get(user_id=request.user.id)
    questionForm=CFORM.QuestionForm() 
    
    if request.method=='POST':
        questionForm=CFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            
            question = questionForm.save(commit=False)
            question.customer=customer
            question.save()
            return redirect('question-history')
    return render(request,'customer/ask_question.html',{'questionForm':questionForm,'Patient':Patient})

def question_history_view(request):
    Patient = models.Patient.objects.get(user_id=request.user.id)
    questions = CMODEL.Question.objects.all().filter(Patient=Patient)
    return render(request,'customer/question_history.html',{'questions':questions,'Patient':Patient})

