from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render, render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from apogeeproj.models import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect,Http404,HttpResponse, JsonResponse
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import json

@csrf_exempt
def user_login(request):

    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_staff:
                login(request, user)
                return HttpResponseRedirect('../timetable/1/')
            else:
                login(request, user)
                return HttpResponseRedirect('../timetable/1/')
        else:
            context = {'error_heading' : "Invalid Login Credentials", 'error_message' :  'Please <a href=".">try again</a>'}
            return render(request, 'apogeeproj/login.html', context)
    else:
        return render(request, 'apogeeproj/login.html')

@login_required
def timetable(request, week_no):
    user = request.user
    lec = Lecture.objects.filter(week_no = week_no, user = user)
    context={
        'lec':lec,
    }
    return render(request, 'apogeeproj/timetable.html', context)
    # return HttpResponse(context)

@login_required
def user_dashboard(request):
    return render(request, 'apogeeproj/dashboard.html')    

@login_required
@csrf_exempt
def save_lec(request):
    if request.method == 'POST':
        attd = request.POST['attd']
        evalu = request.POST['evalu']
        max_marks = int(request.POST['max_marks'])
        marks_obt = int(request.POST['marks_obt'])
        week = request.POST['week']
        hour = request.POST['hour']
        day = request.POST['day']
        sub = int(request.POST['sub'])
        subject = Subject.objects.get(id = sub)
        if attd == True:
            if evalu == True:
                lec = Lecture(user = user, subject = subject, day_no = day, week_no = week, hour_no = hour, attendence = True, evaluative = True, max_marks = max_marks, marks_obt = marks_obt)
                lec.save()
            elif evalu == False:
                lec = Lecture(user = user, subject = subject, day_no = day, week_no = week, hour_no = hour, attendence = True, evaluative = False, max_marks = max_marks, marks_obt = marks_obt)
                lec.save()
        elif attd == False:
            if evalu == True:
                lec = Lecture(user = user, subject = subject, day_no = day, week_no = week, hour_no = hour, attendence = False, evaluative = True, max_marks = max_marks, marks_obt = marks_obt)
                lec.save()
            elif evalu == False:
                lec = Lecture(user = user, subject = subject, day_no = day, week_no = week, hour_no = hour, attendence = False, evaluative = False, max_marks = max_marks, marks_obt = marks_obt)
                lec.save()


@login_required
def calculate_percentage_attd(request, sid):
    user = request.user
    subject = Subject.objects.get(id = sid)
    lec = Lecture.objects.filter(week_no = week_no, user = user, subject = subject)
    all_lec = Lecture.objects.filter(user=user, subject = subject).count()
    max_marks = 0
    marks_obt = 0
    for x in lec:
        if x.attendence == True:
            totattd += 1
            if x.evaluative == True:
                max_marks += x.max_marks
                marks_obt += x.marks_obtained
    percattd = totalattd/all_lec
    percmarks = marks_obt/max_marks
    return percattd

@login_required
def calculate_percentage_marks(request, sid):
    user = request.user
    subject = Subject.objects.get(id = sid)
    lec = Lecture.objects.filter(week_no = week_no, user = user, subject = subject)
    all_lec = Lecture.objects.filter(user=user, subject = subject).count()
    max_marks = 0
    marks_obt = 0
    for x in lec:
        if x.attendence == True:
            totattd += 1
            if x.evaluative == True:
                max_marks += x.max_marks
                marks_obt += x.marks_obtained
    percattd = totalattd/all_lec
    percmarks = marks_obt/max_marks
    return percmarks

@login_required
def calculate_max_marks(request, sid):
    user = request.user
    subject = Subject.objects.get(id = sid)
    lec = Lecture.objects.filter(week_no = week_no, user = user, subject = subject)
    all_lec = Lecture.objects.filter(user=user, subject = subject).count()
    max_marks = 0
    marks_obt = 0
    for x in lec:
        if x.attendence == True:
            totattd += 1
            if x.evaluative == True:
                max_marks += x.max_marks
                marks_obt += x.marks_obtained
    percattd = totalattd/all_lec
    percmarks = marks_obt/max_marks
    return max_marks

@login_required
def cg_pred(request):
    math_attd = calculate_percentage_attd(request, 3)
    bio_attd = calculate_percentage_attd(request, 2)
    chem_attd = calculate_percentage_attd(request, 1)
    math_perc_marks = calculate_percentage_marks(request, 3)
    bio_perc_marks = calculate_percentage_marks(request, 2)
    chem_perc_marks = calculate_percentage_marks(request, 1)
    math_tot_marks = calculate_max_marks(request, 3)
    bio_tot_marks = calculate_max_marks(request, 2)
    chem_tot_marks = calculate_max_marks(request, 1)

# Create your views here.
