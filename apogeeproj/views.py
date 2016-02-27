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
        user = request.user
        attd = request.POST['attd']
        evalu = request.POST['evalu']
        max_marks = request.POST['max_marks']
        marks_obt = request.POST['marks_obt']
        week = request.POST['week']
        hour = request.POST['hour']
        day = request.POST['day']
        sub = int(request.POST['sub'])
        subject = Subject.objects.get(id = sub)
        if attd == 'true':
            if evalu == 'true':
                lec = Lecture(user = user, subject = subject, day_no = day, week_no = week, hour_no = hour, attendence = True, evaluative = True, max_marks = max_marks, marks_obtained = marks_obt)
                lec.save()
            elif evalu == 'false':
                lec = Lecture(user = user, subject = subject, day_no = day, week_no = week, hour_no = hour, attendence = True, evaluative = False, max_marks = max_marks, marks_obtained = marks_obt)
                lec.save()
        elif attd == 'false':
            if evalu == 'true':
                lec = Lecture(user = user, subject = subject, day_no = day, week_no = week, hour_no = hour, attendence = False, evaluative = True, max_marks = max_marks, marks_obtained = marks_obt)
                lec.save()
            elif evalu == 'false':
                lec = Lecture(user = user, subject = subject, day_no = day, week_no = week, hour_no = hour, attendence = False, evaluative = False, max_marks = max_marks, marks_obtained = marks_obt)
                lec.save()
        return HttpResponse(1)

@login_required
def calculate_percentage_attd(request, sid):
    user = request.user
    subject = Subject.objects.get(id = sid)
    lec = Lecture.objects.filter(user = user, subject = subject)
    all_lec = Lecture.objects.filter(user=user, subject = subject).count()
    max_marks = 0.0
    marks_obt = 0.0
    totattd = 0.0
    for x in lec:
        if x.attendence == True:
            totattd += 1.0
            if x.evaluative == True:
                max_marks += x.max_marks
                marks_obt += x.marks_obtained
    percattd = (totattd/all_lec)*100
    percmarks = (marks_obt/max_marks)*100
    return percattd

@login_required
def calculate_percentage_marks(request, sid):
    user = request.user
    subject = Subject.objects.get(id = sid)
    lec = Lecture.objects.filter(user = user, subject = subject)
    all_lec = Lecture.objects.filter(user=user, subject = subject).count()
    max_marks = 0.0
    marks_obt = 0.0
    totattd = 0.0

    for x in lec:
        if x.attendence == True:
            totattd += 1.0
            if x.evaluative == True:
                max_marks += x.max_marks
                marks_obt += x.marks_obtained
    percattd = (totattd/all_lec)*100
    percmarks = (marks_obt/max_marks)*100
    return percmarks

@login_required
def calculate_max_marks(request, sid):
    user = request.user
    subject = Subject.objects.get(id = sid)
    lec = Lecture.objects.filter(user = user, subject = subject)
    all_lec = Lecture.objects.filter(user=user, subject = subject).count()
    max_marks = 0.0
    marks_obt = 0.0
    totattd = 0.0

    for x in lec:
        if x.attendence == True:
            totattd += 1.0
            if x.evaluative == True:
                max_marks += x.max_marks
                marks_obt += x.marks_obtained
    percattd = (totattd/all_lec)*100
    percmarks = (marks_obt/max_marks)*100
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
    math_y = 0.6054*math_attd + 138.21
    math_marks=(((300-math_tot_marks)/300)*math_y)+((math_tot_marks*math_perc_marks)/100)
    chem_y = 0.9467*chem_attd + 121.56
    chem_marks=(((300-chem_tot_marks)/300)*chem_y)+((chem_tot_marks*chem_perc_marks)/100)
    bio_y = 0.7842*bio_attd + 72.79
    bio_marks=(((200-bio_tot_marks)/200)*bio_y)+((bio_tot_marks*bio_perc_marks)/100)
    math_gradelist=[215,195,183,174,143,108,56,0]
    chem_gradelist=[228,207,189,175,150,118,68,0]
    bio_gradelist=[149,138,124,110,85,58,20,0]
    
    if 149<bio_marks<200:
        bgrade = 'A'
        bcg = 10
    elif 138<bio_marks<149:
        bgrade = 'A-'
        bcg = 9
    elif 124<bio_marks<138:
        bgrade = 'B'
        bcg = 8
    elif 110<bio_marks<124:
        bgrade = 'B-'
        bcg = 7
    elif 85<bio_marks<110:
        bgrade = 'C'
        bcg = 6
    elif 58<bio_marks<85:
        bgrade = 'C-'
        bcg = 5
    elif 20<bio_marks<58:
        bgrade = 'D'
        bcg = 4
    elif 0<bio_marks<20:
        bgrade = 'E'
        bcg = 2

    if 215<math_marks<300:
        mgrade = 'A'
        mcg = 10
    elif 195<math_marks<215:
        mgrade = 'A-'
        mcg = 9

    elif 183<math_marks<195:
        mgrade = 'B'
        mcg = 8

    elif 174<math_marks<183:
        mgrade = 'B-'
        mcg = 7

    elif 143<math_marks<174:
        mgrade = 'C'
        mcg = 6

    elif 108<math_marks<143:
        mgrade = 'C-'
        mcg = 5

    elif 56<math_marks<108:
        mgrade = 'D'
        mcg = 4

    elif 0<math_marks<56:
        mgrade = 'E'
        mcg = 2
                   

    if 228<chem_marks<300:
        cgrade = 'A'
        ccg = 10
    elif 207<chem_marks<228:
        cgrade = 'A-'
        ccg = 9

    elif 189<chem_marks<207:
        cgrade = 'B'
        ccg = 8

    elif 175<chem_marks<189:
        cgrade = 'B-'
        ccg = 7

    elif 150<chem_marks<175:
        cgrade = 'C'
        ccg = 6

    elif 118<chem_marks<150:
        cgrade = 'C-'
        ccg = 5

    elif 68<chem_marks<118:
        cgrade = 'D'
        ccg = 4

    elif 0<chem_marks<68:
        cgrade = 'E'
        ccg = 2

    cgpa = (mcg+ccg+bcg)/3
    context = {'math_marks':math_marks,  'chem_marks':chem_marks, 'bio_marks':bio_marks, 'mgrade':mgrade, 'bgrade':bgrade, 'cgrade':cgrade,  'cgpa':cgpa}
    return render(request,'apogeeproj/cgp_final.html', context)
    # Create your views here.
