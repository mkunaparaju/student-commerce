import requests
import os
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.template.context_processors import csrf

from .models import AuthUser

# Create your views here.
#def index(request):
	#r = requests.get('http://httpbin.or
    # c = {}
    # c.update(csrf(request))g/status/418')
	#print r.text
    	#return HttpResponse('<pre>' + r.text + '</pre>')

# def index(request):
# 	times = int(os.environ.get('TIMES',3))
#     	return HttpResponse('Hello! ' * times)
def login_user(request):
    state = "Please log in below..."
    username = password = ''
    c = {}
    c.update(csrf(request))
	
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return render_to_response('auth.html',{'state':state, 'username': username})


def db(request):

    #greeting = Greeting()
    #greeting.save()

    #greetings = Greeting.objects.all()
	
	users = AuthUser.objects.all()
	return render(request, 'db.html', {'users': users})

