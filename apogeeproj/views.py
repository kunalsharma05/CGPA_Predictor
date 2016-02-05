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
                return HttpResponseRedirect('../dashboard/')
            else:
                login(request, user)
                return HttpResponseRedirect('../dashboard/')
        else:
            context = {'error_heading' : "Invalid Login Credentials", 'error_message' :  'Please <a href=".">try again</a>'}
            return render(request, 'apogeeproj/login.html', context)
    else:
        return render(request, 'apogeeproj/login.html')

@login_required
def timetable(request, week_no):
    user = request.user
    lec = Lecture.objects.filter(week_no = week_no)
    context={
        'lec':lec,
    }
    return render(request, 'apogeeproj/timetable.html')

# Create your views here.
